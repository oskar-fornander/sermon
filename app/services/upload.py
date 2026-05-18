import subprocess
import socket
from pathlib import Path
from app.config import SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_KEY, SFTP_REMOTE_PATH, SFTP_URL
from app.errors import ValidationError


def upload_file(local_path):
    """Upload file with sftp"""

    if not SFTP_HOST:
        raise ValidationError("SFTP ej konfigurerat")

    key_file = str(Path(SFTP_KEY).expanduser())

    result = subprocess.run(
        [
            "scp",
            "-i", key_file,
            "-P", SFTP_PORT,
            str(local_path),
            f"{SFTP_USER}@{SFTP_HOST}:{SFTP_REMOTE_PATH}"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"SCP failed:\n{result.stderr}")

    url = SFTP_URL.rstrip('/') + '/' + Path(local_path).name

    return url

