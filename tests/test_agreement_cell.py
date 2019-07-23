import unittest


from .utils.brain import get_brain_with_fallback
from cells.agreement import get_cell


class TestAgreementCell(unittest.TestCase):
    def test_agreed(self):
        brain = get_brain_with_fallback([get_cell()])
        response = brain.respond('yes i will')
        self.assertTrue(response)

    def test_afirmative_sentence(self):
        brain = get_brain_with_fallback([get_cell()])
        response = brain.respond('i am certain about it')
        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
