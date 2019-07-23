from abc import ABC, abstractclassmethod
from dataclasses import dataclass
import paralleldots


from cells.brain import CleanedText
from talking.audio import Recognition
from talking.speech import Speaker
from talking.talk_util import build_summary
import json
import logger


paralleldots.set_api_key(json.load(open('.keys.json'))['paralleldots']['api'])


@dataclass
class ProcessableCell(ABC):
    text: CleanedText
    speaker: Speaker
    recognition: Recognition

    def __post_init__(self):
        self.logging = logger.get_instance()

    @abstractclassmethod
    def process(self):
        pass

    def speak_summary(self, results, name, topic, plural='s'):
        self.speaker.speak(build_summary(results, name, topic, plural=plural))

    def keywords(self):
        keywords = paralleldots.keywords(self.text)['keywords']
        if type(keywords) is list:
            return [item['keyword'] for item in keywords]
        return self.text.clean_text()


@dataclass
class ExecutableCellProxy():
    cell_process: ProcessableCell
    text: CleanedText = None

    def __call__(self, text: CleanedText):
        self.text = text

    def forward(self, speaker, recognition):
        return self.cell_process(self.text, speaker, recognition)
