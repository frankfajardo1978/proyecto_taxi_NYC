from ftplib import FTP_TLS

ftp_host = "72.167.57.128"
ftp_user = "temp@spanishmissionbuilders.com"
ftp_password = "#Connectdata1"  # Reemplaza con tu contraseña

try:
    # Conexión FTPS explícita
    ftps = FTP_TLS()
    ftps.connect(host=ftp_host, port=21, timeout=10)
    ftps.login(user=ftp_user, passwd=ftp_password)
    ftps.prot_p()
    print("Conexión FTPS exitosa.")

    # Subir un archivo
    local_file = "archivo_prueba.txt"  # Archivo local para subir
    with open(local_file, "rb") as file:
        ftps.storbinary(f"STOR {local_file}", file)
    print(f"Archivo {local_file} subido correctamente.")

    # Listar archivos después de subir
    print("Archivos en el servidor:")
    ftps.retrlines("LIST")

    ftps.quit()
except Exception as e:
    print(f"Error al conectar o transferir archivos: {e}")