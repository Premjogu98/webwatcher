from dataclasses import dataclass
from main.logger import console_logger
from main.comparison import Comparison
from main.file_handler import FileHandler
from datetime import datetime

@dataclass
class ConditionHandler:
    QUERY_HANDLER: any
    fileHandler = FileHandler()

    def checkConditionBeforeTextComparison(self, **details):
        oldhtmlfile = f"{details['id']}-oldhtmlfile.html"
        newhtmlfile = f"{details['id']}-newhtmlfile.html"
        
        if not details["oldHtmlPath"] and not details["newHtmlPath"]:
            console_logger.debug("DB Condition 1.....")
            if self.fileHandler.generateHtmlFile(htmlstring=details["onlyhtml"], filename=oldhtmlfile):
                self.QUERY_HANDLER.executeQuery(f"""UPDATE dms_wpw_tenderlinksdata_test SET oldHtmlPath = "{oldhtmlfile}" WHERE id = {details["id"]}""")
                return True
            
        elif details["oldHtmlPath"] and not details["newHtmlPath"]:
            console_logger.debug("DB Condition 2.....")
            _, old_text = self.fileHandler.extractStringFromHtmlFile(filename=oldhtmlfile)
            ObjComparison = Comparison(OLD_TEXT=old_text, NEW_TEXT=details["onlytext"])
            result,compare_per = ObjComparison.startCompare()
            if result:
                if self.fileHandler.generateHtmlFile(htmlstring=details["onlyhtml"],filename=newhtmlfile):
                    self.QUERY_HANDLER.executeQuery(f"""UPDATE dms_wpw_tenderlinksdata_test SET newHtmlPath = "{newhtmlfile}", compare_per = "{str(compare_per)}", compare_changed_on = "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}" WHERE id = {details["id"]}""")
                    return True
                
        elif details["oldHtmlPath"] and details["newHtmlPath"]:
            console_logger.debug("DB Condition 3.....")
            old_html, old_text = self.fileHandler.extractStringFromHtmlFile(newhtmlfile)
            ObjComparison = Comparison(OLD_TEXT=old_text,NEW_TEXT=details["onlytext"])
            result,compare_per = ObjComparison.startCompare()
            if result:
                if self.fileHandler.generateHtmlFile(htmlstring=details["onlyhtml"],filename=newhtmlfile) and self.fileHandler.generateHtmlFile(htmlstring=old_html,filename=oldhtmlfile):
                    self.QUERY_HANDLER.executeQuery(f"""UPDATE dms_wpw_tenderlinksdata_test SET newHtmlPath = "{newhtmlfile}", oldHtmlPath = "{oldhtmlfile}", compare_per = "{str(compare_per)}", compare_changed_on = "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", last_compare_changed_on="{details["compare_changed_on"]}" WHERE id = {details["id"]}""")
                    return True
        else:
            raise Exception("checkConditionBeforeTextComparison NO DB Condition Matched.....")
        
        return False