import mimetypes
import boto3
from botocore.exceptions import NoCredentialsError
from dataclasses import dataclass
from datetime import datetime
import os, parsel, re, sys, time
from pathlib import Path
import requests


from main.global_variables import extractStringFromHTML
from main.logger import console_logger
from main.env_handler import EnvHandler


@dataclass
class FileHandler:
    ACCESS_KEY = EnvHandler.AWS_CRED["ACCESS_KEY"]
    SECRET_KEY = EnvHandler.AWS_CRED["SECRET_KEY"]
    ENDPOINT_URL = EnvHandler.AWS_CRED["ENDPOINT_URL"]
    ACL = EnvHandler.AWS_CRED["ACL"]
    BUCKET = EnvHandler.AWS_CRED["BUCKET"]
    DIRECTORY = "webpagewatcher"
    HTML_DOCS_PATH = os.path.join(os.getcwd(), "htmldocs")
    # blockquotestart = "<Blockquote style='border:1px solid; padding:10px; font-family: 'fontRegular'!important; direction: rtl; text-align: right;'>"
    # blockquotend = "</Blockquote>"

    def generateHtmlFile(self, htmlstring, filename):
        try:
            # Path(self.HTML_DOCS_PATH).mkdir(parents=True, exist_ok=True)
            # File_path = os.path.join(self.HTML_DOCS_PATH, filename)
            # file1 = open(File_path, "w", encoding="utf-8")
            # Final_Doc = f""" <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
            #                 <html xmlns=\"http://www.w3.org/1999/xhtml\">
            #                     <head>
            #                         <meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\" />
            #                         <title>Tender Document</title>
            #                     </head>
            #                     <body>
            #                     { htmlstring if self.blockquotend in htmlstring else f"{self.blockquotestart}{str(htmlstring)}{self.blockquotend}" }
            #                     </body>
            #                 </html>"""
            # file1.write(htmlstring)
            # file1.close()

            s3 = boto3.resource(
                "s3",
                aws_access_key_id=self.ACCESS_KEY,
                aws_secret_access_key=self.SECRET_KEY,
                endpoint_url=self.ENDPOINT_URL,
            )
            key_name = filename
            key_name = self.DIRECTORY + "/" + filename
            object = s3.Object(self.BUCKET, key_name)
            result = object.put(
                Body=htmlstring.encode("utf-8"), ContentType="text/html", ACL=self.ACL
            )
            res = result.get("ResponseMetadata")
            if res.get("HTTPStatusCode") == 200:
                return True
            else:
                raise Exception("Error while uploading files")
        except Exception as e:
            raise Exception(e)

    def getFileName(self, tild):
        Current_dateTime = datetime.now().strftime("%Y%m%d%H%M%S%f")
        Fileid = "".join([str(tild), Current_dateTime])
        return f"{Fileid}.html"

    def extractHtmlElements(self, html_content, xpath_expression):
        selector = parsel.Selector(text=html_content)
        selected_elements = " ".join(selector.xpath(xpath_expression).extract())
        return selected_elements

    def extractInnerText(self, filename: str):
        try:
            # with open(
            #     os.path.join(self.HTML_DOCS_PATH, filename), "r", encoding="utf-8"
            # ) as f:
            #     Extracted_html = f.read()
            #     # Extracted_html = self.extractHtmlElements(
            #     #     html_content=text, xpath_expression="///html/body[1]/blockquote"
            #     # )
            #     return Extracted_html, extractStringFromHTML(Extracted_html)

            response = requests.get(
                f"https://s3.nl.geostorage.net/tottestupload3/webpagewatcher/{filename}"
            )
            response.raise_for_status()  # Raise an exception for HTTP errors (status codes other than 2xx)
            Extracted_html = response.text
            return Extracted_html, extractStringFromHTML(Extracted_html)

        except requests.RequestException as e:
            raise Exception(e)

        except Exception as e:
            raise Exception(e)

    def deleteHtmlFiles(self, filename: str):
        os.remove(os.path.join(self.HTML_DOCS_PATH, filename))
        return True

    def UploadFile(self, filepath, s3dirct=""):
        try:
            content_type = mimetypes.MimeTypes().guess_type(filepath)[0]
            key_names = filepath
            if "\\" in filepath:
                key_nameArr = filepath.split("\\")
                key_names = key_nameArr.pop()  # get last element

            s3 = boto3.resource(
                "s3",
                aws_access_key_id=self.ACCESS_KEY,
                aws_secret_access_key=self.SECRET_KEY,
                endpoint_url=self.ENDPOINT_URL,
            )

            key_name = key_names
            if s3dirct != "":
                key_name = s3dirct + "/" + key_names
            object = s3.Object(self.BUCKET, key_name)

            if content_type != None and content_type != "":
                result = object.put(
                    Body=open(filepath, "rb"), ContentType=content_type, ACL=self.ACL
                )
            else:
                result = object.put(Body=open(filepath, "rb"), ACL=self.ACL)

            res = result.get("ResponseMetadata")
            if res.get("HTTPStatusCode") == 200:
                return True
            else:
                return False

        except NoCredentialsError:
            console_logger.error("\033[91m Credentials not available")
            return False
        except Exception as e:
            console_logger.error(
                "\033[91m EXCEPTION: Error on line {}  EXCEPTION: {} \033[00m".format(
                    sys.exc_info()[-1].tb_lineno, e
                )
            )
            return False

    def upload_to_s3(self, filepath, directory):
        loop = 0
        while loop == 0:
            try:
                result = self.UploadFile(filepath, directory)
                if result == True:
                    loop = 1  # success
                else:
                    console_logger.error("Error while uploading file on S3 Bucket..!")
                    time.sleep(10)
            except Exception as e:
                console_logger.error(
                    "\033[91m EXCEPTION: Error on line {}  EXCEPTION: {} \033[00m".format(
                        sys.exc_info()[-1].tb_lineno, e
                    )
                )
                time.sleep(10)

    def renameFile(self, old_file, new_file):
        try:

            s3 = boto3.client(
                "s3",
                aws_access_key_id=self.ACCESS_KEY,
                aws_secret_access_key=self.SECRET_KEY,
                endpoint_url=self.ENDPOINT_URL,
            )

            s3.copy_object(
                Bucket=self.BUCKET,
                CopySource=f"{self.BUCKET}/{self.DIRECTORY}/{old_file}",
                Key=f"{self.DIRECTORY}/{new_file}",
            )
            s3.delete_object(Bucket=self.BUCKET, Key=old_file)
            console_logger.info(
                f"File '{old_file}' renamed to '{new_file}' successfully."
            )
            return True

        except Exception as e:
            console_logger.error(
                "\033[91m EXCEPTION: Error on line {}  EXCEPTION: {} \033[00m".format(
                    sys.exc_info()[-1].tb_lineno, e
                )
            )
            raise Exception(e)


fileHandler = FileHandler()
