import unittest.mock
import pyttsx3


from .utils.decorator import decorate_with_callback
from talking.speech import Speaker


def mock_speaker_and_return():
    def get_property_mock(text):
        return [] if text == 'voices' else 1

    speech_mock = unittest.mock.Mock()
    speech_mock.getProperty = unittest.mock.MagicMock(side_effect=get_property_mock)
    pyttsx3.init = unittest.mock.MagicMock(return_value=speech_mock)
    speaker = Speaker(None)
    speaker.speak = unittest.mock.MagicMock(side_effect=speaker.speak)
    return speaker


def with_speaker_mocked(fn):
    return decorate_with_callback(fn, mock_speaker_and_return)


if __name__ == '__main__':
    unittest.main()
