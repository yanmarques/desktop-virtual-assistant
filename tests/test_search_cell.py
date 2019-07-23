import unittest


from .utils.brain import BrainPatchTestCase
from cells.search import get_cell


class TestSearchCell(BrainPatchTestCase):
    def test_specific_search(self):
        # patch brain with a cell search that just return the text
        brain = self._patch(get_cell(), lambda text: text)
        response = brain.respond('I am searching for foo')
        self.assertEqual(response.clean_text(), ['foo'])


if __name__ == '__main__':
    unittest.main()
