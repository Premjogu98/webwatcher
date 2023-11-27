from dataclasses import dataclass
from main.logger import console_logger
from main.comparison.ocr import OpticalCharacterRecognition


@dataclass
class Comparison:
    OLD_TEXT: str
    NEW_TEXT: str

    def startCompare(self):
        opticalCharacterRecognition = OpticalCharacterRecognition(
            OLD_TEXT=self.OLD_TEXT, NEW_TEXT=self.NEW_TEXT
        )
        return opticalCharacterRecognition.calculateSimilarity()
