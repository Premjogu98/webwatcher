from dataclasses import dataclass
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(os.path.join(os.getcwd(), ".env"))
load_dotenv(dotenv_path=dotenv_path)


@dataclass
class EnvHandler:
    MARK = "ww".upper()
    DB_CONNECTION = {
        "DB_HOST": os.getenv(f"{MARK}_DB_IP"),
        "DB_USERNAME": os.getenv(f"{MARK}_DB_USERNAME"),
        "DB_PASSWORD": os.getenv(f"{MARK}_DB_PASSWORD"),
        "DB_NAME": os.getenv(f"{MARK}_DB_NAME"),
    }
    AWS_CRED = {
        "ACCESS_KEY": os.getenv(f"{MARK}_AWS_ACCESS_KEY"),
        "SECRET_KEY": os.getenv(f"{MARK}_AWS_SECRET_KEY"),
        "ENDPOINT_URL": os.getenv(f"{MARK}_AWS_ENDPOINT_URL"),
        "ACL": os.getenv(f"{MARK}_AWS_ACL"),
        "BUCKET": os.getenv(f"{MARK}_AWS_BUCKET"),
    }
