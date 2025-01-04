#CICLO DE VIDA DEL DATO

##FUENTE
- Se obtiene el dato directamente del cliente en formato CSV o Parquet

##EXTRACCION
- La extraccion se basa principalmente con un bucket utilizado en Google Cloud.
- Extrae directamente al bucket creado.
- Extrae con nombre de archivo original.

## VERIFICACION
- Nuestra función solo procesa archivos con las extensiones .csv, .xlsx (Excel), o .parquet, si el archivo tiene otro formato, se detiene el proceso.

## CREACION DE CARPETA TEMPORAL

- El archivo se descarga desde el bucket y se guarda temporalmente en la carpeta /tmp del entorno de la Cloud Function.

## LECTURA DE ARCHIVO

- Mediante la libreria de pandas se procede asignar un dataframe al archivo abierto.

## TRANSFORMACION DE DATOS

### Normalizacion de nombres de columnas

- Se eliminan espacios y se convierten los nombres de columnas a minúsculas para estandarizar.

### Manejo de valores inválidos

- Datos categoricos: Se eliminan caracteres no imprimibles y se rellenan valores faltantes con "N/A".

- Datos numericos: Enteros (int) y flotantes (float): Se convierten valores no válidos a NaN o 0 y se rellenan según corresponda.

## Guardado de archivo transformado
- Se guarda el DataFrame transformado en un archivo temporal (en este punto se incorpora un codigo que trasnforme cualquier caracter no imprimible en el nombre del archivo para evtar cualquier inconveniente en la futura creacion de tablas en Big Querry).

## Subida de archivo transformado a GCS

- El archivo transformado se sube al bucket en una carpeta llamada transformed/.

## Carga de datos en BigQuery

### Configuracion de BigQuery

- Se configura un dataset y una tabla en BigQuery. El dataset se basa en el nombre del archivo (De igual manera se ingresa un parametro que reemplace cualquier caracter no imprimible para evitar problemas en la creacion del dataset y tabla).

### Creacion del dataset si no existe

- Crea el dataset en el servicio de Big Querry de Google Cloud basado en el nombre del archivo original en caso de que no exista.

### Definicion de esquema y cargar datos
- Se crean columnas y filas dependiendo de la estructura de los datos del dataset

### Eliminar archivos temporales

- Con cada proceso se elimina la carpeta /temp. del entorno de Google Cloud.

## FINALIZACION 

Si el evento se finaliza correctamente el entorno devuelve el print ("Proceso ETL completado exitosamente.") garantizando el ETL y la devolucion de tablas en Big Querry, lo que a su vez nos sirve como  verificacion y validacion del proceso.

