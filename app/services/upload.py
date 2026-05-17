import paramiko
import socket
from pathlib import Path
from app.config import SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASSWORD, SFTP_KEY, SFTP_REMOTE_PATH
from app.errors import ValidationError


def upload_file(local_path: str):
    """Upload file with sftp"""

    if not SFTP_HOST:
        raise ValidationError("SFTP ej konfigurerat")

    print('1')
    #transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    sock = socket.create_connection((SFTP_HOST, SFTP_PORT), timeout=10)
    transport = paramiko.Transport(sock)




    print('2')
    if SFTP_KEY:
        key = paramiko.RSAKey.from_private_key_file(Path(SFTP_KEY).expanduser())
        transport.connect(username=SFTP_USER, pkey=key)
    else:
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)


    print('3')

    sftp = paramiko.SFTPClient.from_transport(transport)


    print('4')

    remote_file = f"{SFTP_REMOTE_PATH}/{Path(local_path).name}"

    sftp.put(local_path, remote_file)

    sftp_close()
    transport.close()

    return remote_file

