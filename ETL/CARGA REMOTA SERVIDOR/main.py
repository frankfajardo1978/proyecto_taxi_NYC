from ftplib import FTP_TLS
from google.cloud import storage
import os

def fetch_and_upload_all_from_ftp(request):
    """
    Descarga todos los archivos de un servidor FTP y los sube a Google Cloud Storage automáticamente.

    Variables de entorno requeridas:
        - FTP_HOST: Dirección del servidor FTP.
        - FTP_USER: Usuario del servidor FTP.
        - FTP_PASSWORD: Contraseña del servidor FTP.
        - GCS_BUCKET: Nombre del bucket de destino en GCS.
    """
    # Leer credenciales y configuraciones desde el entorno
    ftp_host = os.environ.get('FTP_HOST')
    ftp_user = os.environ.get('FTP_USER')
    ftp_password = os.environ.get('FTP_PASSWORD')
    target_bucket = os.environ.get('GCS_BUCKET')

    if not all([ftp_host, ftp_user, ftp_password, target_bucket]):
        return "Faltan variables de entorno necesarias.", 400

    # Conexión FTPS explícita
    ftps = FTP_TLS()
    try:
        ftps.connect(host=ftp_host, port=21, timeout=10)
        ftps.login(user=ftp_user, passwd=ftp_password)
        ftps.prot_p()
        print(f"Conexión exitosa al servidor FTP: {ftp_host}")

        # Listar archivos en el directorio actual y filtrar solo archivos
        file_list = []

        # Usar MLSD para obtener detalles de cada entrada
        ftps.retrlines("MLSD", file_list.append)  
        print(f"Entradas encontradas en el FTP: {file_list}")

        # Lista de extensiones permitidas
        allowed_extensions = [".csv", ".parquet", ".json", ".txt"]

        # Filtrar solo archivos con extensiones permitidas
        files_to_process = []
        for entry in file_list:
            parts = entry.split(";")  # Dividir la entrada para analizar atributos
            if "type=file" in parts:  # Verificar si es un archivo
                filename = parts[-1].strip()  # Buscar nombre de archivo
                if any(filename.endswith(ext) for ext in allowed_extensions):  # Verificar extensiones
                    files_to_process.append(filename)

        print(f"Archivos a procesar: {files_to_process}")

        if not files_to_process:
            return "No se encontraron archivos en el servidor FTP.", 200

        # Inicializar cliente de Google Cloud Storage
        client = storage.Client()
        bucket = client.bucket(target_bucket)

        # Procesar cada archivo
        for remote_file_path in files_to_process:
            # Descargar archivo remoto
            temp_file = f"/tmp/{os.path.basename(remote_file_path)}"
            with open(temp_file, "wb") as file:
                ftps.retrbinary(f"RETR {remote_file_path}", file.write)
            print(f"Archivo descargado: {remote_file_path}")

            # Generar nombre del blob en GCS basado en el nombre del archivo
            target_blob_name = f"{os.path.basename(remote_file_path)}"

            # Subir archivo a GCS (sobreescribe si ya existe)
            blob = bucket.blob(target_blob_name)
            blob.upload_from_filename(temp_file)
            print(f"Archivo subido a gs://{target_bucket}/{target_blob_name}")

            # Eliminar archivo temporal
            os.remove(temp_file)

        ftps.quit()
        return f"Todos los archivos fueron procesados y subidos a gs://{target_bucket}", 200
    except Exception as e:
        return f"Error al conectar o transferir archivos: {e}", 500
