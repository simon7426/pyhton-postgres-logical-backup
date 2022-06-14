# Python script to backup a postgres database to S3

This python script will perform a logical backup of a postgres instance to S3. A logical backup translates all the data into a set of SQL commands and writes it into a single file. This sql file can then be fed into another databse to recreate everything. It is a simple and quicker way to backup a database. It can come in handy when migrating from one postgres version to another. The biggest drawback of logical backups is that, one cannot perform point in time recovery(PITR) using a logical backup.

## Installation

If using poetry,

```console
poetry install
```

or if using pip,

```console
pip install -r requirements.txt
```

## Backing up the databse

Set the environment variables in .env file. Then, to backup the database. Run the following commands.
If using poetry,

```console
poetry run python app.py backup
```

Without poetry,

```console
python app.py backup
```

## TODO

1. Restore databse.
2. List databse currently uploaded in s3.
