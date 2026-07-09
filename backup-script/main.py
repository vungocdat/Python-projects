import datetime
import subprocess
import tarfile

import docker

backup_dir = "/home/mecha/backups"
today = datetime.date.today()


def backup_vw():
    """
    function will stop vaulwarden container, start a new temporary docker container and mount the
    vaulwarden data, tar the entire volume and stop the tmp container and removes it. then start
    the vaulwarden again.
    """
    dk = docker.from_env()
    backup_path = f"{backup_dir}/vw"
    vaultwarden = dk.containers.get("vaultwarden")
    vw_data = dk.volumes.get("vaultwarden_vw_data")
    custom_tar_command = f"tar czf /backup/vw_data.tar-{today}.gz -C /data ."

    vaultwarden.stop()

    try:
        dk.containers.run(
            "alpine",
            custom_tar_command,
            remove=True,
            volumes={
                vw_data.name: {"bind": "/data", "mode": "ro"},
                backup_path: {"bind": "/backup", "mode": "rw"},
            },
        )
    finally:
        vaultwarden.start()


def backup_kb():
    """
    Stop the KB service, backup the data (SQL Lite DB) and then start the KV service again
    """
    service_name = "dt-kb.service"
    backup_name = f"{backup_dir}/dt-kb/kb.db.tar-{today}.gz"
    file_location = "/opt/dt-kb/data/kb.db"

    subprocess.run(["systemctl", "stop", service_name], check=True)
    try:
        with tarfile.open(backup_name, "w:gz") as tar:
            tar.add(file_location, arcname="kb.db")
    finally:
        subprocess.run(["systemctl", "start", service_name], check=True)


backup_vw()
backup_kb()
