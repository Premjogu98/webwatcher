from dataclasses import dataclass
from main.logger import console_logger
from main.comparison import Comparison
from main.file_handler import FileHandler
from main.global_variables import GlobalVariable
from main.db_connection.query_handler import QueryHandler
from datetime import datetime
from main.env_handler import EnvHandler
from typing import Dict, Any


@dataclass
class ConditionHandler:
    QUERY_HANDLER: QueryHandler
    GLOBAL_VARIABLE: GlobalVariable
    fileHandler: FileHandler = FileHandler()

    def updateChangesCount(self, id: int) -> None:
        self.QUERY_HANDLER.executeQuery(
            f"UPDATE dms_wpw_tenderlinksdata SET changes_count = changes_count + 1 WHERE id = {id}"
        )

    @staticmethod
    def getCurrentTime() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def getDatetimeDifference(first: str, second: str) -> float:
        time_difference = datetime.strptime(
            second, "%Y-%m-%d %H:%M:%S"
        ) - datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        return time_difference.total_seconds() / 60

    def checkConditionBeforeTextComparison(self, **details: Dict[str, Any]) -> bool:
        oldhtmlfile = f"{details['tlid']}-oldhtmlfile.html"
        newhtmlfile = f"{details['tlid']}-newhtmlfile.html"

        if not details["newHtmlPath"]:
            return self._handle_condition_1(details, newhtmlfile)
        elif not details["oldHtmlPath"] and details["newHtmlPath"]:
            return self._handle_condition_2(details, oldhtmlfile, newhtmlfile)
        elif details["oldHtmlPath"] and details["newHtmlPath"]:
            return self._handle_condition_3(details, oldhtmlfile, newhtmlfile)
        else:
            raise Exception(
                "checkConditionBeforeTextComparison NO DB Condition Matched....."
            )

    def _handle_condition_1(self, details: Dict[str, Any], newhtmlfile: str) -> bool:
        console_logger.debug("DB Condition 1.....")
        if self.fileHandler.generateHtmlFile(
            htmlstring=details["onlyhtml"], filename=newhtmlfile
        ):
            self.QUERY_HANDLER.executeQuery(
                f"""UPDATE dms_wpw_tenderlinksdata SET newHtmlPath = "{newhtmlfile}", entrydone = "N", error_date = "", compare_error = "" WHERE id = {details["id"]}"""
            )
            self.GLOBAL_VARIABLE.nothing_changed += 1
            return True
        return False

    def _handle_condition_2(
        self, details: Dict[str, Any], oldhtmlfile: str, newhtmlfile: str
    ) -> bool:
        console_logger.debug("DB Condition 2.....")

        """UPDATE dms_wpw_tenderlinksdata SET oldHtmlPath = "{oldhtmlfile}", newHtmlPath = "{newhtmlfile}", 
        compare_per = "{compare_per}", CompareChangedOn = "{self.getCurrentTime()}", 
        entrydone = "N", error_date = "", compare_error = "" WHERE id = {details["id"]}"""

        _, old_text = self.fileHandler.extractInnerText(filename=details["newHtmlPath"])
        return self._compare_and_update(details, old_text, oldhtmlfile, newhtmlfile)

    def _handle_condition_3(
        self, details: Dict[str, Any], oldhtmlfile: str, newhtmlfile: str
    ) -> bool:
        console_logger.debug("DB Condition 3.....")

        """UPDATE dms_wpw_tenderlinksdata SET newHtmlPath = "{newhtmlfile}", oldHtmlPath = "{oldhtmlfile}", 
        compare_per = "{compare_per}", CompareChangedOn = "{self.getCurrentTime()}", LastCompareChangedOn="{details["CompareChangedOn"]}",
        entrydone = "N" , error_date = "", compare_error = "" WHERE id = {details["id"]}"""

        _, old_text = self.fileHandler.extractInnerText(details["newHtmlPath"])
        return self._compare_and_update(
            details, old_text, oldhtmlfile, newhtmlfile, is_condition_3=True
        )

    def _compare_and_update(
        self,
        details: Dict[str, Any],
        old_text: str,
        oldhtmlfile: str,
        newhtmlfile: str,
        is_condition_3: bool = False,
    ) -> bool:
        obj_comparison = Comparison(OLD_TEXT=old_text, NEW_TEXT=details["onlytext"])
        result, compare_per = obj_comparison.startCompare()
        if result and self._rename_and_generate_files(
            details["newHtmlPath"], oldhtmlfile, details["onlyhtml"], newhtmlfile
        ):
            self._update_database(
                details, oldhtmlfile, newhtmlfile, compare_per, is_condition_3
            )
            self.updateChangesCount(id=details["id"])
            self.GLOBAL_VARIABLE.compared += 1
            return True
        self.GLOBAL_VARIABLE.nothing_changed += 1
        return False

    def _rename_and_generate_files(
        self, old_path: str, oldhtmlfile: str, onlyhtml: str, newhtmlfile: str
    ) -> bool:
        return self.fileHandler.renameFile(
            old_file=old_path, new_file=oldhtmlfile
        ) and self.fileHandler.generateHtmlFile(
            htmlstring=onlyhtml, filename=newhtmlfile
        )

    def _update_database(
        self,
        details: Dict[str, Any],
        oldhtmlfile: str,
        newhtmlfile: str,
        compare_per: float,
        is_condition_3: bool,
    ) -> None:
        query = f"""UPDATE dms_wpw_tenderlinksdata SET 
                    newHtmlPath = "{newhtmlfile}", 
                    oldHtmlPath = "{oldhtmlfile}", 
                    compare_per = "{str(compare_per)}", 
                    CompareChangedOn = "{self.getCurrentTime()}", 
                    {"LastCompareChangedOn='"+details["CompareChangedOn"]+"'," if is_condition_3 else ""}
                    entrydone = "N", 
                    error_date = "", 
                    compare_error = "" 
                    WHERE id = {details["id"]}"""
        self.QUERY_HANDLER.executeQuery(query)
