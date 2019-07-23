import unittest


from .utils.brain import get_brain_with_fallback
from cells.greetings import get_cell


class TestInstallCell(unittest.TestCase):
    def test_greeting(self):
        cell = get_cell()
        cell.responses = 'bar'
        brain = get_brain_with_fallback([cell])
        response = brain.respond('hey you')
        self.assertEqual(response, 'bar')


if __name__ == '__main__':
    unittest.main()
