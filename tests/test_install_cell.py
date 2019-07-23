import unittest.mock


from .utils.brain import BrainPatchTestCase
from .test_shell import get_mock_process, mock_pexpect_and_return, with_getpass_mocked
from .test_speaker import with_speaker_mocked
from .test_audio import mock_recognition_and_return
from cells.brain import CleanedText
from cells.install import get_cell, InstallProcess


def get_install_process(speaker, recognition, text='install foo',
                      additional_stopwords=['install']):
    cleaned_text = CleanedText(text, additional_stopwords)
    return InstallProcess(cleaned_text, speaker, recognition)


class TestInstallCell(BrainPatchTestCase):
    def test_package_discover(self):
        # patch brain with a cell installation that just return the
        # text stemmed
        brain = self._patch(get_cell(), lambda text: text)
        response = brain.respond('can you install foo please')
        self.assertEqual(response.clean_text(), ['foo'])

    def test_multiple_package_discover(self):
        brain = self._patch(get_cell(), lambda text: text)
        response = brain.respond('make the installation of foo, baz and bar please')
        self.assertEqual(response.clean_text(), ['foo', 'baz', 'bar'])

    def test_not_choose_to_install(self):
        # always return foo when reach the installation
        brain = self._patch(get_cell(), lambda text: 'foo')
        response = brain.respond('the way you make is annoying')
        self.assertNotEqual(response, 'foo')

    @with_getpass_mocked
    @with_speaker_mocked
    def test_install_cell_process_directly(self, getpass_mock, speaker_mock):
        spawn_mock = mock_pexpect_and_return(
                        return_value=get_mock_process(password_prompt=False))
        recognition_mock = mock_recognition_and_return(return_value='yes')

        installation = get_install_process(speaker_mock, recognition_mock)
        installation.process()

        spawn_mock.assert_called_once_with('sudo dnf install -y foo', encoding='utf-8')
        self.assertEqual(speaker_mock.speak.call_count, 3)

    @with_getpass_mocked
    @with_speaker_mocked
    def test_install_cell_process_with_unknow_package(self, getpass_mock, speaker_mock):
        spawn_mock = mock_pexpect_and_return(
                        return_value=get_mock_process(password_prompt=False,
                                        before='Unable to find a match'))
        recognition_mock = mock_recognition_and_return(return_value='yes')

        installation = get_install_process(speaker_mock, recognition_mock)
        installation.process()

        self.assertEqual(speaker_mock.speak.call_count, 4)

    @with_getpass_mocked
    @with_speaker_mocked
    def test_install_cell_process_with_many_known_packages(self, getpass_mock,
                                                           speaker_mock):
        spawn_mock = mock_pexpect_and_return(
                        return_value=get_mock_process(password_prompt=False))
        recognition_mock = mock_recognition_and_return(return_value='yes')

        installation = get_install_process(speaker_mock, recognition_mock,
                                           text='install foo bar')
        installation.process()

        # 2 static calls then 1 call for each package
        self.assertEqual(speaker_mock.speak.call_count, 2 + 1 * 2)


if __name__ == '__main__':
    unittest.main()
