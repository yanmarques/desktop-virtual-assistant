import pyttsx3


import logger


class Speaker():
    def __init__(self, lang, female=True):
        self.speech = pyttsx3.init('espeak')
        self.logging = logger.get_instance()
        self._configure(lang, female)

    def speak(self, text):
        self.logging.info(f'new speech: {text}')
        self.speech.say(text)
        self.speech.runAndWait()

    def _configure(self, lang: str, female: bool):
        rate = self.speech.getProperty('rate')
        self.speech.setProperty('rate', rate - 85)

        voices = self.speech.getProperty('voices')
        for voice in voices:
            if voice.id == lang:
                voice_id = voice.id
                if female:
                    voice_id += '+f3'
                self.speech.setProperty('voice', voice_id)
                break
