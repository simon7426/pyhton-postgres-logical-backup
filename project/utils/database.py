import subprocess


def list_postgres_databases(host, database_name, port, user, password):
    try:
        process = subprocess.Popen(
            [
                "psql",
                "--dbname=postgresql://{}:{}@{}:{}".format(user, password, host, port),
                "--list",
            ],
            stdout=subprocess.PIPE,
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            print("Command failed. Return code : {}".format(process.returncode))
            exit(1)
        return output
    except Exception as e:
        print(e)
        exit(1)


def set_postgres_password(password):
    try:
        process = subprocess.Popen(
            ["export", "PGPASSWORD={}".format(password)], stdout=subprocess.PIPE
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            print("Command failed. Return code : {}".format(process.returncode))
            exit(1)
        return output
    except Exception as e:
        print(e)
        exit(1)
