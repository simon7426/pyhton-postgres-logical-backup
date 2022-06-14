import os

from dotenv import load_dotenv


class BaseConfig:
    load_dotenv()
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    BACKUP_PATH = "./"
    VERBOSE = os.getenv("VERBOSE", "False").lower() in ("true", "1", "t")
    ACCESS_KEY = os.getenv("ACCESS_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    S3_ENDPOINT = os.getenv("S3_ENDPOINT")
    print(S3_ENDPOINT)
