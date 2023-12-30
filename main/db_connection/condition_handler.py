from dataclasses import dataclass
from main.logger import console_logger
from main.comparison import Comparison
from main.file_handler import FileHandler
from main.global_variables import GlobalVariable
from main.db_connection.query_handler import QueryHandler
from datetime import datetime
from main.env_handler import EnvHandler
@dataclass
class ConditionHandler:
    QUERY_HANDLER: QueryHandler
    GLOBAL_VARIABLE: GlobalVariable
    fileHandler = FileHandler()
    
    def updateChangesCount(self,id):
        self.QUERY_HANDLER.executeQuery(f"""UPDATE dms_wpw_tenderlinksdata SET changes_count = changes_count + 1 WHERE id = {id}""")

    def getCurrentTime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def getDatetimeDifference(self, first, second):
        start_time = datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(second, "%Y-%m-%d %H:%M:%S")
        time_difference = end_time - start_time
        return time_difference.total_seconds() / 60
    
    def checkConditionBeforeTextComparison(self, **details):
        oldhtmlfile = f"{details['id']}-oldhtmlfile.html"
        newhtmlfile = f"{details['id']}-newhtmlfile.html"
        
        if not details["oldHtmlPath"] and not details["newHtmlPath"]:
            # console_logger.debug("DB Condition 1.....")
            if self.fileHandler.generateHtmlFile(htmlstring=details["onlyhtml"], filename=oldhtmlfile):
                self.QUERY_HANDLER.executeQuery(f"""UPDATE dms_wpw_tenderlinksdata SET oldHtmlPath = "{oldhtmlfile}" WHERE id = {details["id"]}""")
                self.GLOBAL_VARIABLE.nothing_changed += 1
                return True
            
        elif details["oldHtmlPath"] and not details["newHtmlPath"]:
            # console_logger.debug("DB Condition 2.....")

            _, old_text = self.fileHandler.extractInnerText(filename=oldhtmlfile)
            ObjComparison = Comparison(OLD_TEXT=old_text, NEW_TEXT=details["onlytext"])
            result,compare_per = ObjComparison.startCompare()
            if result:
                if self.fileHandler.generateHtmlFile(htmlstring=details["onlyhtml"],filename=newhtmlfile):
                    self.QUERY_HANDLER.executeQuery(f"""UPDATE dms_wpw_tenderlinksdata SET newHtmlPath = "{newhtmlfile}", compare_per = "{str(compare_per)}", CompareChangedOn = "{self.getCurrentTime.strftime("%Y-%m-%d %H:%M:%S")}", entrydone = "N" WHERE id = {details["id"]}""")
                    self.updateChangesCount(id=details["id"])
                    self.GLOBAL_VARIABLE.compared += 1
                    return True
                
        elif details["oldHtmlPath"] and details["newHtmlPath"]:
            # console_logger.debug("DB Condition 3.....")
            old_html, old_text = self.fileHandler.extractInnerText(newhtmlfile)
            ObjComparison = Comparison(OLD_TEXT=old_text,NEW_TEXT=details["onlytext"])
            result,compare_per = ObjComparison.startCompare()
            if result:
                if self.fileHandler.generateHtmlFile(htmlstring=details["onlyhtml"],filename=newhtmlfile) and self.fileHandler.generateHtmlFile(htmlstring=old_html,filename=oldhtmlfile):
                    self.QUERY_HANDLER.executeQuery(f"""UPDATE dms_wpw_tenderlinksdata SET newHtmlPath = "{newhtmlfile}", oldHtmlPath = "{oldhtmlfile}", compare_per = "{str(compare_per)}", CompareChangedOn = "{self.getCurrentTime.strftime("%Y-%m-%d %H:%M:%S")}", LastCompareChangedOn="{details["CompareChangedOn"]}", entrydone = "N" WHERE id = {details["id"]}""")
                    self.updateChangesCount(id=details["id"])
                    self.GLOBAL_VARIABLE.compared += 1
                    return True
        else:
            raise Exception("checkConditionBeforeTextComparison NO DB Condition Matched.....")
        
        # self.GLOBAL_VARIABLE.nothing_changed += 1
        return False