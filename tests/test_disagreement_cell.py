import unittest


from .utils.brain import get_brain_with_fallback
from cells.disagreement import get_cell


class TestDisagreementCell(unittest.TestCase):
    def test_disagree(self):
        brain = get_brain_with_fallback([get_cell()])
        response = brain.respond('no i won\'t')
        self.assertFalse(response)

    def test_negative_sentence(self):
        brain = get_brain_with_fallback([get_cell()])
        response = brain.respond('i refuse to be certain')
        self.assertFalse(response)


if __name__ == '__main__':
    unittest.main()
