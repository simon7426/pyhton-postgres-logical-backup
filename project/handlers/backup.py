import datetime

from project.configs import BaseConfig
from project.utils.backup import backup_postgres_db, clean_file, compress_file
from project.utils.s3 import get_s3_client, upload_to_s3


def backup_postgres_handler(logger):
    config = BaseConfig()
    host = config.POSTGRES_HOST
    port = config.POSTGRES_PORT
    user = config.POSTGRES_USER
    password = config.POSTGRES_PASSWORD
    postgres_db = config.DB_NAME
    backup_path = config.BACKUP_PATH
    verbose = config.VERBOSE
    access_key = config.ACCESS_KEY
    secret_key = config.SECRET_KEY
    bucket_name = config.BUCKET_NAME
    endpoint = config.S3_ENDPOINT

    bucket_path = datetime.datetime.now().strftime("%Y%m%d")

    timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = "backup-{}-{}.dump".format(timestr, postgres_db)
    filename_compressed = "{}.gz".format(filename)
    local_file_path = "{}{}".format(backup_path, filename)

    logger.info(
        "Backing up {} database to {}".format(f"{host}:{port}", local_file_path)
    )

    _ = backup_postgres_db(
        host=host,
        port=port,
        user=user,
        password=password,
        dest_file=local_file_path,
        verbose=verbose,
        logger=logger,
    )

    logger.info("Backup complete")
    logger.info("Compressing {}".format(local_file_path))
    comp_file = compress_file(local_file_path)
    logger.info("Uploading {} to Amazon S3...".format(comp_file))
    s3_client = get_s3_client(
        access_key=access_key, aws_secret_key=secret_key, endpoint=endpoint
    )
    upload_to_s3(
        s3_client=s3_client,
        bucket_name=bucket_name,
        bucket_path=bucket_path,
        file_full_path=comp_file,
        dest_file=filename_compressed,
    )
    logger.info("Uploaded to {}".format(filename_compressed))
    logger.info("Cleaning up {}".format(local_file_path))
    clean_file(local_file_path, logger)
