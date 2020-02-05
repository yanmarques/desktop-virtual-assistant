import shell
import re


import cells
import executable_cell
from .brain import CellStemmerExecutor


class InstallProcess(executable_cell.ProcessableCell):
    def process(self):
        self.logging.info('installation process initiated')
        bin_brain = cells.get_binary_brain(False)
        packages = self.keywords()
        packages = [pkg.replace(' ', '') for pkg in packages]
        self.logging.debug(f'packages to be installed: {packages}')

        self.speak_summary(packages, 'package', 'to install')
        self.speaker.speak('do you want a direct install?')
        response = self.recognition.listen_repeatdly()
        if response:
            if bin_brain.respond(response):
                list(map(self._direct_install, packages))
            else:
                pass

    def _direct_install(self, package):
        self.logging.info(f'installing {package}')
        def handle_pwd(attempts):
            if attempts > 0:
                message = 'last saved password failed, fill with a password'
            else:
                message = 'you must fill the password'
            self.speaker.speak(message)

        self.speaker.speak(f'executing installation for {package}')
        args = f'dnf install -y {package}'
        process = shell.run(args, on_pwd=handle_pwd, root=True)
        
        if process.before is None:
            if process.after is None:
                self.speaker.speak('maybe this package is already installed')
        elif re.match(r'Unable to find a match', process.before):
            self.speaker.speak(f'any result found on repository for {package}')


def get_cell():
    patterns = ['install', 'installation', 'make install', 'proceed installing']
    executable = executable_cell.ExecutableCellProxy(InstallProcess)
    return CellStemmerExecutor(patterns=patterns, 
                                stem_patterns=True,
                                executable=executable)
