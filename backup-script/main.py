import datetime
import subprocess
import tarfile
import os
import docker

vw_dir = '/home/mecha/backups/vw'
kb_dir = '/home/mecha/backups/dt-kb'
today = datetime.date.today()


def backup_vw():
    """
    function will stop vaulwarden container, start a new temporary docker container and mount the
    vaulwarden data, tar the entire volume and stop the tmp container and removes it. then start
    the vaulwarden again.
    """
    dk = docker.from_env()
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
                vw_dir: {"bind": "/backup", "mode": "rw"},
            },
        )
    finally:
        vaultwarden.start()


def backup_kb():
    """
    Stop the KB service, backup the data (SQL Lite DB) and then start the KV service again
    """
    service_name = "dt-kb.service"
    backup_name = f"{kb_dir}/kb.db.tar-{today}.gz"
    file_location = "/opt/dt-kb/data/kb.db"

    subprocess.run(["systemctl", "stop", service_name], check=True)
    try:
        with tarfile.open(backup_name, "w:gz") as tar:
            tar.add(file_location, arcname="kb.db")
    finally:
        subprocess.run(["systemctl", "start", service_name], check=True)


def backup_cleaup(backup_dir):
    """
    Take path to backup files, then delete the old files an keeps only 10 backup files
    """
    os.chdir(backup_dir)
    backup_files = os.listdir()
    sorted_files = sorted(backup_files, reverse=True, key=lambda file_name: os.path.getmtime(file_name))
    if len(sorted_files) > 10:
        old_files = sorted_files[10:]
        for old in old_files:
            os.remove(old)


backup_vw()
backup_kb()
backup_cleaup(vw_dir)
backup_cleaup(kb_dir)
