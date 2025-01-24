from flask import Flask, request, jsonify, render_template
from google.cloud import storage
import os
from time import sleep

app = Flask(__name__)

# Credenciales de Google Cloud
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/service-account-key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/service-account-key-PF.json"

BUCKET_NAME = "prueba2frank"
# En caso de algún cambio: Reemplazar con el nombre del bucket de GCS  

# Carga la interfaz web
@app.route('/')
def index():
    return render_template('index.html')

# Backend para subir archivos a GCS
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se encontró el archivo", 400

    file = request.files['file']
    if file.filename == '':
        return "El nombre del archivo está vacío", 400

    # Conecta con Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file.filename)

    # Subir el archivo al bucket
    
    # Barra de progreso
    with blob.open("wb") as f:
        chunk_size = 1024 * 1024  # 1 MB por chunk
        file_stream = file.stream

        while chunk := file_stream.read(chunk_size):
            f.write(chunk)
            
    # Confirmación de subida
    return f"Archivo '{file.filename}' subido exitosamente", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
