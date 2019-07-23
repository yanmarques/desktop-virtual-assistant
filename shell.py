import pexpect
import getpass


import logger


LOGGER = logger.get_instance()


def run(command, arguments=[], expect_eof=False, root=False, on_pwd=None):
    if root:
        command = 'sudo ' + command
    LOGGER.debug(f'calling: {command}')
    process = pexpect.spawn(command, encoding='utf-8')
    attempts = 0
    while process.waitnoecho(2.5):
        if attempts > 0:
            LOGGER.info('password has failed')
        else:
            LOGGER.info('password required for command')
        if on_pwd is not None:
            on_pwd(attempts)
        LOGGER.debug('sending password to process')
        process.sendline(getpass.getpass())
        attempts += 1
    if expect_eof:
        process.expect(pexpect.EOF)
    LOGGER.debug('command finished')
    return process
