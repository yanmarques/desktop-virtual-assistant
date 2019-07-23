from .brain import CellStemmerExecutor
from executable_cell import ProcessableCell, ExecutableCellProxy


class SearchProcess(ProcessableCell):
    def process(self):
        print('searching: ' + str(self.text))
        keywords = self.keywords()
        print(keywords)


def get_cell():
    patterns = ['search', 'searching', 'finding', 'find', 'look for', 'locate',
               'looking for']
    return CellStemmerExecutor(patterns=patterns, stem_patterns=True,
                               executable=ExecutableCellProxy(SearchProcess))
