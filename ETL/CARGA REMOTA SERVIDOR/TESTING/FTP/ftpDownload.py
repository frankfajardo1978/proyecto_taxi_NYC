from ftplib import FTP_TLS

ftp_host = "72.167.57.128"
ftp_user = "temp@spanishmissionbuilders.com"
ftp_password = "#Connectdata1"

try:
    # Conexión FTPS explícita
    ftps = FTP_TLS()
    ftps.connect(host=ftp_host, port=21, timeout=10)
    ftps.login(user=ftp_user, passwd=ftp_password)
    ftps.prot_p()
    print("Conexión FTPS exitosa.")

    # Descargar un archivo
    remote_file = "archivo_prueba.txt"  # Archivo en el servidor
    local_file = "descargado_archivo_prueba.txt"  # Nombre local para guardar
    with open(local_file, "wb") as file:
        ftps.retrbinary(f"RETR {remote_file}", file.write)
    print(f"Archivo {remote_file} descargado como {local_file}.")

    ftps.quit()
except Exception as e:
    print(f"Error al conectar o transferir archivos: {e}")