from ftplib import FTP_TLS

ftp_host = "72.167.57.128"
ftp_user = "temp@spanishmissionbuilders.com"
ftp_password = "#Connectdata1"  # Reemplaza con la contraseña real

try:
    # Conexión FTPS explícita
    ftps = FTP_TLS()
    print(f"Conectando a {ftp_host}...")
    ftps.connect(host=ftp_host, port=21, timeout=10)  # Conexión al puerto 21
    ftps.login(user=ftp_user, passwd=ftp_password)
    ftps.prot_p()  # Cambiar a modo de protección de datos segura
    print("Conexión FTPS exitosa.")

    # Listar archivos en el directorio raíz
    print("Archivos en el directorio raíz:")
    ftps.retrlines("LIST")
    
    # Cerrar conexión
    ftps.quit()
except Exception as e:
    print(f"Error al conectar: {e}")
