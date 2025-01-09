from google.cloud import storage, bigquery
import pandas as pd
import os
import numpy as np
import hashlib

def calculate_file_hash(file_path):
    """
    Calcula el hash SHA256 de un archivo.

    Args:
        file_path (str): Ruta al archivo.

    Returns:
        str: Hash SHA256 del archivo.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def etl_process(event, context):
    """
    Cloud Function que realiza un proceso ETL cuando se sube un archivo al bucket.

    Args:
        event (dict): Datos del evento de GCS.
        context (google.cloud.functions.Context): Contexto del evento.
    """
    # Extraer información del evento
    bucket_name = event['bucket']
    file_name = event['name']

    # Verificar el tipo de archivo
    if not (file_name.endswith('.csv') or file_name.endswith('.xlsx') or file_name.endswith('.parquet')):
        print(f"El archivo {file_name} no es un CSV, Excel o Parquet. Se omite el procesamiento.")
        return

    # Descargar el archivo desde el bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    local_file_path = f"/tmp/{file_name}"
    blob.download_to_filename(local_file_path)
    print(f"Archivo descargado: {local_file_path}")

    # Leer el archivo según su formato con manejo de errores
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(local_file_path, on_bad_lines='skip', quotechar='"', encoding_errors='replace')
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(local_file_path)
        elif file_name.endswith('.parquet'):
            df = pd.read_parquet(local_file_path)
    except Exception as e:
        print(f"Error al leer el archivo {file_name}: {e}")
        return

    # Transformar: Normalizar nombres de columnas
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

    # Transformar: Manejar valores inválidos o no procesables
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].replace({r'[^ -~]': 'N/A'}, regex=True)
            df[col] = df[col].fillna("N/A").astype(str)
        elif pd.api.types.is_integer_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        elif pd.api.types.is_float_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(np.nan).astype(float)
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(np.nan)

    # Agregar un identificador único (hash de fila) para cada registro
    df['row_hash'] = df.apply(lambda row: hashlib.sha256(str(row.values).encode('utf-8')).hexdigest(), axis=1)

    # Guardar el archivo transformado temporalmente y en la carpeta "transformed" del bucket
    transformed_dir = "/tmp/transformed"
    os.makedirs(transformed_dir, exist_ok=True)
    transformed_file = f"{transformed_dir}/{file_name.replace('+', '_')}"

    if file_name.endswith('.csv'):
        df.to_csv(transformed_file, index=False)
    elif file_name.endswith('.parquet'):
        df.to_parquet(transformed_file, index=False)

    transformed_blob_path = f"transformed/{file_name.replace('+', '_')}"
    transformed_blob = bucket.blob(transformed_blob_path)
    transformed_blob.upload_from_filename(transformed_file)
    print(f"Archivo transformado subido a GCS: gs://{bucket_name}/{transformed_blob_path}")

    # Configurar BigQuery
    dataset_name = file_name.split('.')[0].replace(' ', '_').replace('-', '_').replace('+', '_').lower()
    table_name = "data"
    bq_client = bigquery.Client()

    # Crear el dataset si no existe
    dataset_ref = bq_client.dataset(dataset_name)
    try:
        bq_client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "us-central1"
        bq_client.create_dataset(dataset)
        print(f"Dataset creado: {dataset_name}")

    # Verificar si la tabla principal existe, si no, crearla y cargar todos los datos
    table_ref = dataset_ref.table(table_name)
    try:
        bq_client.get_table(table_ref)
    except Exception:
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        print(f"Tabla creada y datos iniciales cargados: {dataset_name}.{table_name}")
        return

    # Subir datos nuevos a una tabla temporal en BigQuery
    temp_table_name = f"{table_name}_temp"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = bq_client.load_table_from_dataframe(df, dataset_ref.table(temp_table_name), job_config=job_config)
    job.result()
    print(f"Datos subidos temporalmente a BigQuery: {dataset_name}.{temp_table_name}")

    # Realizar un MERGE para insertar solo las filas nuevas en la tabla principal
    merge_query = f"""
    MERGE `{dataset_name}.{table_name}` T
    USING `{dataset_name}.{temp_table_name}` S
    ON T.row_hash = S.row_hash
    WHEN NOT MATCHED THEN
      INSERT ROW
    """

    try:
        query_job = bq_client.query(merge_query)
        query_job.result()  # Espera a que termine el trabajo de la consulta

        # Obtener las estadísticas del trabajo
        if query_job.state == 'DONE':
            rows_affected = query_job.num_dml_affected_rows  # Obtiene el número de filas afectadas
            print(f"Filas nuevas insertadas en la tabla principal: {rows_affected}")
        else:
            print(f"Error en la consulta: {query_job.error_result}")
        print(f"Datos nuevos insertados en la tabla principal: {dataset_name}.{table_name}")
    except Exception as e:
        print(f"Error durante el MERGE en BigQuery: {e}")
        return

    # Eliminar archivos temporales
    try:
        os.remove(local_file_path)
        os.remove(transformed_file)
        print(f"Archivo temporal eliminado: {local_file_path}")
    except Exception as e:
        print(f"Error al eliminar archivos temporales: {e}")

    print("Proceso ETL completado exitosamente.")
