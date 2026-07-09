import docker


def backup_vw():
    """
    function will stop vaulwarden container, start a new temporary docker container and mount the
    vaulwarden data, tar the entire volume and stop the tmp container and removes it. then start
    the vaulwarden again.
    """
    dk = docker.from_env()
    backup_dir = "/home/mecha/backups/vw"
    vaultwarden = dk.containers.get("vaultwarden")
    vw_data = dk.volumes.get("vaultwarden_vw_data")

    vaultwarden.stop()

    dk.containers.run(
        "alpine",
        "tar czf /backup/vw_data.tar.gz -C /data .",
        remove=True,
        volumes={
            vw_data.name: {"bind": "/data", "mode": "ro"},
            backup_dir: {"bind": "/backup", "mode": "rw"},
        },
    )

    vaultwarden.start()


def backup_kb():
    pass


backup_vw()
backup_kb()
