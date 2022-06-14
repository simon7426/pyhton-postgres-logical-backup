import gzip
import os
import subprocess


def backup_postgres_db(host, port, user, password, dest_file, verbose, logger):
    """
    Backup postgres db to a file.
    Steps executed in this function:
    1. To connect to a postgres database seamlessly PGPASSWORD variable is set.
    2. Depending on verbose setting, -v tag is added to the command.
    3. pg_dumpall is called in a subprocess to create the logical backup of the whole database.
    """
    my_env = os.environ.copy()
    my_env["PGPASSWORD"] = password

    commands = [
        "pg_dumpall",
        "--dbname=postgresql://{}:{}@{}:{}".format(user, password, host, port),
        "-c",
        "-f",
        dest_file,
    ]
    if verbose:
        commands.append("-v")

    try:
        process = subprocess.Popen(
            commands,
            stdout=subprocess.PIPE,
            env=my_env,
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            logger.error("Command failed. Return code : {}".format(process.returncode))
            exit(1)
        return output
    except Exception as e:
        logger.error(e)
        exit(1)


def compress_file(src_file):
    """
    Compress the src_file in gunzip format to reduce it's size.
    """
    compressed_file = "{}.gz".format(str(src_file))
    with open(src_file, "rb") as f_in:
        with gzip.open(compressed_file, "wb") as f_out:
            for line in f_in:
                f_out.write(line)
    return compressed_file


def clean_file(file_path, logger):
    """
    Cleaning up redundant files after backup to s3 is complete
    """
    try:
        os.remove(file_path)
    except Exception as e:
        logger.error(e)
        exit(1)
