import mimetypes
import boto3
from botocore.exceptions import ClientError
from dataclasses import dataclass
from datetime import datetime
import os, parsel, re, sys
from pathlib import Path
import requests

from main.global_variables import extractStringFromHTML
from main.logger import console_logger
from main.env_handler import EnvHandler

from typing import Tuple, Optional

@dataclass
class FileHandler:
    ACCESS_KEY: str = EnvHandler.AWS_CRED["ACCESS_KEY"]
    SECRET_KEY: str = EnvHandler.AWS_CRED["SECRET_KEY"]
    ENDPOINT_URL: str = EnvHandler.AWS_CRED["ENDPOINT_URL"]
    ACL: str = EnvHandler.AWS_CRED["ACL"]
    BUCKET: str = "tottestupload3"
    DIRECTORY: str = "webpagewatcher"
    HTML_DOCS_PATH: str = os.getcwd()

    def _get_s3_resource(self):
        return boto3.resource(
            "s3",
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY,
            endpoint_url=self.ENDPOINT_URL,
        )

    def _get_s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY,
            endpoint_url=self.ENDPOINT_URL,
        )

    def generateHtmlFile(self, htmlstring: str, filename: str) -> bool:
        try:
            key_name = f"{self.DIRECTORY}/{filename}"
            s3 = self._get_s3_resource()
            object = s3.Object(self.BUCKET, key_name)
            result = object.put(
                Body=str(htmlstring),
                ContentType="text/html; charset=utf-8",
                ACL=self.ACL,
            )
            res = result.get("ResponseMetadata")
            console_logger.info(f"{filename} File created")
            return res.get("HTTPStatusCode") == 200
        except Exception as e:
            self._log_exception(e)
            raise

    def deleteFileFromS3(self, fileDirectory: str, data: Optional[str] = None) -> None:
        try:
            s3 = self._get_s3_client()
            s3.put_object(
                Bucket=self.BUCKET,
                Key=fileDirectory,
                Body=data,
                ContentType="text/html; charset=utf-8",
            )
            s3.get_object(Bucket=self.BUCKET, Key=fileDirectory)
        except ClientError as e:
            console_logger.error(e)

    @staticmethod
    def getFileName(tild: str) -> str:
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{tild}{current_datetime}.html"

    @staticmethod
    def extractHtmlElements(html_content: str, xpath_expression: str) -> str:
        selector = parsel.Selector(text=html_content)
        return " ".join(selector.xpath(xpath_expression).extract())

    def extractInnerText(self, filename: str) -> Tuple[str, str]:
        try:
            response = requests.get(
                f"https://s3.nl.geostorage.net/{self.BUCKET}/{self.DIRECTORY}/{filename}"
            )
            response.raise_for_status()
            extracted_html = response.text
            return extracted_html, extractStringFromHTML(extracted_html)
        except requests.RequestException as e:
            raise Exception(e)
        except Exception as e:
            self._log_exception(e)
            raise

    def deleteHtmlFiles(self, filename: str) -> bool:
        os.remove(os.path.join(self.HTML_DOCS_PATH, filename))
        return True

    def UploadFile(self, filepath: str) -> bool:
        try:
            content_type = mimetypes.guess_type(filepath)[0]
            key_name = f"{self.DIRECTORY}/{os.path.basename(filepath)}"
            s3 = self._get_s3_resource()
            object = s3.Object(self.BUCKET, key_name)

            with open(filepath, "rb") as file:
                result = object.put(
                    Body=file,
                    ContentType=content_type or "text/html; charset=utf-8",
                    ACL=self.ACL,
                )

            return result.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200
        except Exception as e:
            self._log_exception(e)
            return False

    def upload_to_s3(self, filepath: str, directory: str) -> None:
        while True:
            try:
                if self.UploadFile(filepath):
                    break
                console_logger.error("Error while uploading file on S3 Bucket..!")
            except Exception as e:
                self._log_exception(e)

    def renameFile(self, old_file: str, new_file: str) -> bool:
        try:
            s3 = self._get_s3_client()
            s3.copy_object(
                Bucket=self.BUCKET,
                CopySource=f"{self.BUCKET}/{self.DIRECTORY}/{old_file}",
                Key=f"{self.DIRECTORY}/{new_file}",
            )
            s3.delete_object(Bucket=self.BUCKET, Key=old_file)
            console_logger.info(f"File '{old_file}' renamed to '{new_file}' successfully.")
            return True
        except Exception as e:
            self._log_exception(e)
            raise

    def _log_exception(self, e: Exception) -> None:
        console_logger.error(
            f"\033[91m EXCEPTION: Error on line {sys.exc_info()[-1].tb_lineno}  EXCEPTION: {e} \033[00m"
        )

fileHandler = FileHandler()