import difflib
from difflib import SequenceMatcher
from dataclasses import dataclass
from main.logger import console_logger


@dataclass
class OpticalCharacterRecognition:
    OLD_TEXT: str
    NEW_TEXT: str
    
    # calculate text similarity ratio
    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        similarity_ratio = SequenceMatcher(None, self.OLD_TEXT, self.NEW_TEXT).ratio()
        similarity_ratio_in_per = int(similarity_ratio) * 100
        console_logger.debug(f"Match Percentage => {similarity_ratio_in_per}% / 1.0%")

        if similarity_ratio == "1.0" or similarity_ratio_in_per == 0:
            return False, similarity_ratio_in_per
        return True, similarity_ratio_in_per

    # Print differences with highlighting
    def highlightDifference(self):
        differ = difflib.Differ()
        diff = list(differ.compare(self.OLD_TEXT, self.NEW_TEXT))
        for item in diff:
            if item.startswith("- "):  # Deletion
                console_logger.debug("\033[91m" + item[2:] + "\033[0m", end="")
            elif item.startswith("+ "):  # Addition
                pass
                console_logger.debug("\033[92m" + item[2:] + "\033[0m", end="")
            else:
                console_logger.debug(item[2:], end="")