import subprocess
import socket
from pathlib import Path
from app.config import SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_KEY, WEB_ROOT, WEB_URL
from app.errors import ValidationError


def upload_file(local_path, remote_path, remote_name=''):
    """Upload file with sftp"""
    if remote_name:
        remote_path += '/' + remote_name

    if not SFTP_HOST:
        raise ValidationError("SFTP ej konfigurerat")

    key_file = str(Path(SFTP_KEY).expanduser())

    result = subprocess.run(
        [
            "scp",
            "-i", key_file,
            "-P", SFTP_PORT,
            str(local_path),
            f"{SFTP_USER}@{SFTP_HOST}:{WEB_ROOT}/{remote_path}"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Misslyckades att ladda upp fil till server:\n{result.stderr}")

    return f"{WEB_URL}/{remote_path}"


def delete_file(remote_path):
    """Delete file on remote server via ssh"""
    if not SFTP_HOST:
        raise ValidationError("SFTP ej konfigurerat")

    key_file = str(Path(SFTP_KEY).expanduser())

    remote_file = f"{WEB_ROOT}/{remote_path}"

    result = subprocess.run(
        [
            "ssh",
            "-i", key_file,
            "-p", str(SFTP_PORT),
            f"{SFTP_USER}@{SFTP_HOST}",
            f"rm -f '{remote_file}'"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Misslyckades att radera fil på server:\n{result.stderr}")

    return True


