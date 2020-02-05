import unittest.mock
import time
import pexpect
import getpass


from .utils.decorator import decorate_with_callback
import shell


def get_mock_process(password_prompt=True, before='foo baz'):
    process_mock = unittest.mock.Mock()
    process_mock.waitnoecho = unittest.mock.MagicMock(return_value=password_prompt)
    process_mock.before = before
    return process_mock


def mock_pexpect_and_return(**kwargs):
    spawn_mock = unittest.mock.MagicMock(**kwargs)
    pexpect.spawn = spawn_mock
    return spawn_mock


def mock_getpass_and_return(password='bar'):
    getpass_mock = unittest.mock.MagicMock(return_value=password)
    getpass.getpass = getpass_mock
    return getpass_mock


def with_getpass_mocked(fn):
    return decorate_with_callback(fn, mock_getpass_and_return)


class TestShell(unittest.TestCase):
    @with_getpass_mocked
    def test_run_command_with_password(self, getpass_mock):
        process_mock = get_mock_process()
        sendline_mock = unittest.mock.MagicMock()
        process_mock.sendline = sendline_mock

        def stop_on_first(attempts):
            if attempts == 1:
                process_mock.waitnoecho = unittest.mock.MagicMock(
                                                        return_value=False)

        spawn_mock = mock_pexpect_and_return(return_value=process_mock)
        cmd = 'touch foo'
        shell.run(cmd, on_pwd=stop_on_first)

        spawn_mock.assert_called_once_with(cmd, encoding='utf-8')
        sendline_mock.assert_called_with(getpass_mock.return_value)
        self.assertEqual(getpass_mock.call_count, 2)

    def test_run_command_with_root(self):
        spawn_mock = mock_pexpect_and_return(
                        return_value=get_mock_process(password_prompt=False))

        cmd = 'touch baz'
        shell.run(cmd, root=True)
        spawn_mock.assert_called_once_with(f'sudo {cmd}', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
