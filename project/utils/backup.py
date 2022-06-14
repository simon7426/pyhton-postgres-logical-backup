import gzip
import os
import subprocess


def backup_postgres_db(host, port, user, password, dest_file, verbose, logger):
    """
    Backup postgres db to a file.
    """
    my_env = os.environ.copy()
    my_env["PGPASSWORD"] = password

    if verbose:
        try:
            process = subprocess.Popen(
                [
                    "pg_dumpall",
                    "--dbname=postgresql://{}:{}@{}:{}".format(
                        user, password, host, port
                    ),
                    "-c",
                    "-f",
                    dest_file,
                    "-v",
                ],
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
    else:

        try:
            process = subprocess.Popen(
                [
                    "pg_dumpall",
                    "--dbname=postgresql://{}:{}@{}:{}".format(
                        user, password, host, port
                    ),
                    "-f",
                    dest_file,
                ],
                stdout=subprocess.PIPE,
                env=my_env,
            )
            output = process.communicate()[0]
            if process.returncode != 0:
                logger.error("Command failed. Return code : {}".format(process.returncode))
                exit(1)
            return output
        except Exception as e:
            logger.error(e)
            exit(1)


def compress_file(src_file):
    compressed_file = "{}.gz".format(str(src_file))
    with open(src_file, "rb") as f_in:
        with gzip.open(compressed_file, "wb") as f_out:
            for line in f_in:
                f_out.write(line)
    return compressed_file


def clean_file(file_path, logger):
    try:
        os.remove(file_path)
    except Exception as e:
        logger.error(e)
        exit(1)
