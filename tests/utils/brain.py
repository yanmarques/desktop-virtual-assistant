import unittest


from cells.brain import CellChoice, IdentifiablePatternCell, CellStemmerExecutor


def get_brain_with_fallback(cells):
    return CellChoice(cells, IdentifiablePatternCell('Fallback message'))


def get_random_cell(responses='foo', patterns=['bar'], executable=None):
    if executable is not None:
        return CellStemmerExecutor(executable=executable, responses=responses,
                                   patterns=patterns)
    return IdentifiablePatternCell(responses=responses, patterns=patterns)


class BrainPatchTestCase(unittest.TestCase):
    def _patch(self, cell, function):
        cell.executable = function
        return get_brain_with_fallback([cell])
