import unittest.mock
import speech_recognition


from talking.audio import Recognition


def mock_recognition_and_return(**kwargs):
    recognition = Recognition(None)
    recognition.recognizer.recognize_google = unittest.mock.MagicMock(**kwargs)
    recognition.recognizer.listen = unittest.mock.MagicMock()
    return recognition


if __name__ == '__main__':
    unittest.main()
