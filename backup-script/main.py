import datetime
import subprocess
import tarfile
import os
import stat
import docker

vw_dir = '/home/mecha/backups/vw'
kb_dir = '/home/mecha/backups/dt-kb'
today = datetime.date.today()


def set_permissions(file_path):
    """
    change the file owner and group - mecha on the server has uid and gid 1000
    change the file permissions to 640
    """
    uid = 1000
    gid = 1000
    os.chown(file_path, uid, gid)
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)


def backup_vw():
    """
    function will stop vaulwarden container, start a new temporary docker container and mount the
    vaulwarden data, tar the entire volume and stop the tmp container and removes it. then start
    the vaulwarden again.
    """
    dk = docker.from_env()
    vaultwarden = dk.containers.get("vaultwarden")
    vw_data = dk.volumes.get("vaultwarden_vw_data")
    custom_tar_command = f"tar czf /backup/vw_data-{today}.tar.gz -C /data ."
    new_backup_file = f"{vw_dir}/vw_data-{today}.tar.gz"

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
        set_permissions(new_backup_file)
    finally:
        vaultwarden.start()


def backup_kb():
    """
    Stop the KB service, backup the data (SQL Lite DB) and then start the KV service again
    """
    service_name = "dt-kb.service"
    backup_name = f"{kb_dir}/kb.db-{today}.tar.gz"
    file_location = "/opt/dt-kb/data/kb.db"

    subprocess.run(["systemctl", "stop", service_name], check=True)
    try:
        with tarfile.open(backup_name, "w:gz") as tar:
            tar.add(file_location, arcname="kb.db")

        set_permissions(backup_name)
    finally:
        subprocess.run(["systemctl", "start", service_name], check=True)


def backup_cleaup(backup_dir):
    """
    Take path to backup files, then delete the old files an keeps only 10 backup files.
    dot_clean list ensure that the list does not contains the hidden files
    """
    backup_files = os.listdir(backup_dir)
    dot_clean = [os.path.join(backup_dir, file) for file in backup_files if not file.startswith('.')]
    sorted_files = sorted(dot_clean, reverse=True, key=lambda file_name: os.path.getmtime(file_name))
    if len(sorted_files) > 10:
        old_files = sorted_files[10:]
        for old in old_files:
            os.remove(old)


backup_vw()
backup_kb()
backup_cleaup(vw_dir)
backup_cleaup(kb_dir)
