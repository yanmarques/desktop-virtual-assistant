import unittest


import cells
from .utils.brain import get_brain_with_fallback, get_random_cell


class TestBrain(unittest.TestCase):
        def test_fallback(self):
            brain = cells.get_brain(fallback_msg='foo')
            response = brain.respond('meaningless')
            self.assertEqual(response, 'foo')

        def test_identifiable_cell_id_equals_skill_responses(self):
            cell = get_random_cell()
            skill = cell.get_pattern_matching_skill()
            self.assertEqual(skill.responses, [cell.identifier])

        def test_identifiable_cell_value_with_string(self):
            cell = get_random_cell()
            self.assertEqual(cell.get_value('bar'), 'foo')

        def test_identifiable_cell_value_with_a_list(self):
            responses = ['foo', 'baz']
            cell = get_random_cell(responses=responses)
            self.assertTrue(cell.get_value('bar') in responses)

        def test_executor_cell_on_function(self):
            cell = get_random_cell(executable=lambda text: 'foo')
            brain = get_brain_with_fallback([cell])
            response = brain.respond('bar')
            self.assertEqual(response, 'foo')

        def test_executor_cell_with_stem_enabled(self):
            # executable just return the text for testing
            cell = get_random_cell(executable=lambda text: text)
            cell.stem_patterns = True
            response = cell.get_value('foo bar')
            self.assertEqual(response.clean_text(), ['foo'])

        def test_executor_cell_without_executable(self):
            cell = get_random_cell(executable='')

            # now set executable to null
            cell.executable = None
            with self.assertRaises(Exception):
                cell.get_value('foo')


if __name__ == '__main__':
    unittest.main()
