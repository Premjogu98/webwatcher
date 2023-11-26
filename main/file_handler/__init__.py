from dataclasses import dataclass
from main.logger import console_logger
from datetime import datetime
import os, parsel, re
from pathlib import Path

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
                                    {self.blockquotestart}{str(htmlstring)}{self.blockquotend}
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

    def extractStringFromHtmlFile(self, filename: str):
        try:
            with open(
                os.path.join(self.htmldocs_path, filename), "r", encoding="utf-8"
            ) as f:
                text = f.read()
                selector = parsel.Selector(text=text)
                html_list = selector.xpath(f"///html/body[1]/blockquote").get()
                text_list = selector.xpath(
                    f"///html/body[1]/blockquote//text()"
                ).getall()
                text_with_space = " ".join(
                    [i.replace("\n", " ").replace("\t", " ") for i in text_list]
                )
                text_with_html = "".join(
                    [
                        i.replace("\n", " ")
                        .replace("\t", " ")
                        .replace(self.blockquotestart, " ")
                        .replace(self.blockquotend, " ")
                        for i in text_list
                    ]
                )
                onlyhtml = re.sub("\s\s+", " ", text_with_html)
                onlytext = re.sub("\s\s+", " ", text_with_space)
                if text_list and html_list:
                    return onlyhtml, onlytext
                else:
                    return False
        except Exception as e:
            raise Exception(e)

    def deleteHtmlFiles(self, filename: str):
        os.remove(os.path.join(self.htmldocs_path, filename))
        return True


fileHandler = FileHandler()
