from dataclasses import dataclass
from main.logger import console_logger
from datetime import datetime
import os, parsel, re
from pathlib import Path
from main.global_variables import extractStringFromHTML


@dataclass
class FileHandler:
    htmldocs_path = os.path.join(os.getcwd(), "htmldocs")
    blockquotestart = "<Blockquote style='border:1px solid; padding:10px; font-family: 'fontRegular'!important; direction: rtl; text-align: right;'>"
    blockquotend = "</Blockquote>"

    def generateHtmlFile(self, htmlstring, filename):
        try:
            Path(self.htmldocs_path).mkdir(parents=True, exist_ok=True)
            File_path = os.path.join(self.htmldocs_path, filename)
            file1 = open(File_path, "w", encoding="utf-8")
            Final_Doc = f""" <!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
                            <html xmlns=\"http://www.w3.org/1999/xhtml\">
                                <head>
                                    <meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\" />
                                    <title>Tender Document</title>
                                </head>
                                <body>
                                { htmlstring if self.blockquotend in htmlstring else f"{self.blockquotestart}{str(htmlstring)}{self.blockquotend}" }
                                </body>
                            </html>"""
            file1.write(Final_Doc)
            file1.close()
            return True
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
            with open(
                os.path.join(self.htmldocs_path, filename), "r", encoding="utf-8"
            ) as f:
                text = f.read()
                Extracted_html = self.extractHtmlElements(
                    html_content=text, xpath_expression="///html/body[1]/blockquote"
                )
                return Extracted_html, extractStringFromHTML(Extracted_html)
        except Exception as e:
            raise Exception(e)

    def deleteHtmlFiles(self, filename: str):
        os.remove(os.path.join(self.htmldocs_path, filename))
        return True


fileHandler = FileHandler()
