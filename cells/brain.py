from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from nltk.corpus import stopwords
from dataclasses import dataclass, field, InitVar
from typing import Any, List
import secrets
import re


def read_stopwords_file():
    with open('stopwords.txt') as words_buffer:
        return words_buffer.readlines()


@dataclass
class IdentifiablePatternCell():
    responses: Any
    patterns: Any = None
    identifier: str = field(default_factory=lambda: secrets.token_hex(12),
                            init=False)

    def get_pattern_matching_skill(self):
        return PatternMatchingSkill(responses=self.identifier,
                                    patterns=self.patterns)

    def get_value(self, text):
        if type(self.responses) is not list:
            return self.responses
        return secrets.choice([self.responses] if type(self.responses)
                              is str else self.responses)


@dataclass
class CellStemmerExecutor(IdentifiablePatternCell):
    executable: Any = None
    responses: Any = None
    stem_patterns: bool = False

    def get_value(self, text):
        if self.executable is None:
            raise Exception('An executable is necessary.')

        stopwords = []
        if self.stem_patterns:
            for pattern in self.patterns:
                stopwords.extend(pattern.split(' '))

        # remove duplicate
        stopwords = list(set(stopwords))

        return self.executable(CleanedText(text, additional_stopwords=stopwords))


@dataclass
class CellChoice():
    cells: List[IdentifiablePatternCell]
    fallback: IdentifiablePatternCell

    def __post_init__(self):
        self.cells.append(self.fallback)
        skills = [cell.get_pattern_matching_skill() for cell in self.cells]
        self.agent = DefaultAgent(skills)

    def respond(self, text: str):
        text = text.lower()
        response = self.agent([text])
        cell = self.find_cell_by_id(response[0])
        if cell is not None:
            return cell.get_value(text)

    def find_cell_by_id(self, identifier):
        for cell in self.cells:
            if cell.identifier == identifier:
                return cell


@dataclass
class CleanedText():
    text: str
    additional_stopwords: InitVar[list] = []

    stopwords = stopwords.words('english') + read_stopwords_file()
    special_chars = re.compile(r'[^a-zA-Z0-9\s_.-]')

    def __post_init__(self, additional_stopwords):
        self.stopwords = self.stopwords + additional_stopwords

    def clean_text(self):
        text = self.special_chars.sub('', self.text)
        return [word for word in text.split()
                if not self.matches_stopword(word)]

    def matches_stopword(self, word):
        for stopword in self.stopwords:
            if word in stopword: return True
        return False

    def __str__(self):
        return self.text
