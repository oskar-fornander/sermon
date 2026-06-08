import subprocess
import socket
from pathlib import Path
from app.config import SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_KEY, WEB_ROOT, WEB_URL
from app.errors import ValidationError


def upload_file(local_path, remote_path, remote_name):
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
            f"{SFTP_USER}@{SFTP_HOST}:{WEB_ROOT}/{remote_path}/{remote_name}"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"SCP failed:\n{result.stderr}")

    return f"{WEB_URL}/{remote_path}"

