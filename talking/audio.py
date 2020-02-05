import speech_recognition


from .speech import Speaker
import logger


class Recognition():
    def __init__(self, speaker: Speaker, listen_repeat_limit: int=3):
        self.listen_repeat_limit = listen_repeat_limit
        self.speaker = speaker
        self.recognizer = speech_recognition.Recognizer()
        self.listen_count = 0
        self.logging = logger.get_instance()
        self._configure()

    def listen_in_background(self, function):
        microphone = speech_recognition.Microphone()
        with microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        return self.recognizer.listen_in_background(microphone, function,
                                                    phrase_time_limit=0.3)

    def listen_repeatdly(self, **kwargs):
        if self.is_last_listen():
            self.logging.info('listener exiting without success')
            self.reset_count()
            return False

        self.listen_count += 1
        self.logging.debug('opening microphone')

        with speech_recognition.Microphone() as source:
            self.recognizer.pause_threshold = 1
            self.logging.debug('adjusting micro against ambient noise')
            self.recognizer.adjust_for_ambient_noise(source)

            self.logging.info('capturing audio')
            audio = self.recognizer.listen(source)

        unknow_msg = 'Could not understand. Can you repeat please?'

        def listen_wrapper():
            return self.listen_repeatdly(**kwargs)

        return self.recognize_audio(audio, listen_wrapper, unknow_msg=unknow_msg,
                                    **kwargs)

    def recognize_audio(self, audio, callback_error, unknow_msg=None, **kwargs):
        try:
            self.logging.info('trying to decode audio to text format')
            response = self.recognizer.recognize_google(audio, **kwargs)
            self.reset_count()
            self.logging.debug(f'recognition successful: {response}')
            return response
        except speech_recognition.UnknownValueError:
            self.logging.error('decoding has failed')
            if unknow_msg:
                self.speaker.speak(unknow_msg)
            return callback_error()
        except speech_recognition.RequestError as e:
            self.logging.error(f'Request error: {e}')

    def reset_count(self):
        self.listen_count = 0

    def is_last_listen(self):
        return self.listen_count >= self.listen_repeat_limit

    def _configure(self):
        self.recognizer.enery_threshold = 200
        self.recognizer.dynamic_energy_threshold = False
