import re
import time


from talking.speech import Speaker
from talking.audio import Recognition
from executable_cell import ExecutableCellProxy
import cells


# class SolutionFinder():
#     def __init__(self, results, show_max_results=5, iteration_sleep=1):
#         self.results = results
#         self.show_max_results = show_max_results
#         self.iteration_sleep = iteration_sleep
#         self.solution_index = None
#         self.current_result = 0
#         m = sr.Microphone()
#         with m as source:
#             r.adjust_for_ambient_noise(source)
#         self.stop = r.listen_in_background(m, self.decision_callback,
#                                            phrase_time_limit=0.3)
#
#     def decision_callback(self, recognizer, audio):
#         noaction = lambda: None
#         response = recognize_audio(audio, noaction, recognizer=recognizer)
#         print(response)
#         if response is not None:
#             if 'this one' in response:
#                 self.stop_on_current_result()
#             elif 'last one' in response:
#                 self.stop_on_current_result(minus=1)
#             elif 'stop' in response:
#                 s.stop()
#                 raise Exception('stopped')
#
#     def stop_on_current_result(self, plus=None, minus=None):
#         current = self.current_result
#         if plus:
#             current += plus
#         if minus:
#             current -= minus
#         self.solution_index = current
#         s.stop()
#
#     def find(self):
#         length = self.show_max_results
#         results_length = len(self.results)
#         self.iterate(length)
#
#         while not self.is_selected() or results_length > length:
#             speak('Do you want me to show more?')
#             response = listen(show_all=True)
#             confident_response = response['alternative'][0]['transcript']
#             if 'yes' in confident_response:
#                 initial_length = length
#                 length += self.show_max_results
#                 self.iterate(length, initial=initial_length)
#             else:
#                 if re.match(r'.*select.*', confident_response):
#                     for alternative in response['alternative']:
#                         index = None
#                         for word in alternative['transcript'].split():
#                             try:
#                                 index = int(word) - 1
#                                 break
#                             except ValueError:
#                                 pass
#                         if index is not None:
#                             self.solution_index = index
#                             break
#         self.stop()
#         if self.is_selected():
#             return self.get_result()
#
#     def iterate(self, end, initial=0):
#         for index, name in enumerate(self.results[initial:end]):
#             if self.is_selected(): return
#             index += initial
#             speak(f'Result number {index + 1}')
#
#             if self.is_selected(): return
#             speak(name.decode('utf-8').split(':')[1].strip())
#
#             if self.is_selected(): return
#
#             self.current_result = index - 1
#             time.sleep(self.iteration_sleep)
#
#     def is_selected(self):
#         return self.solution_index is not None
#
#     def get_result(self):
#         return self.results[self.solution_index]


def main():
    speaker = Speaker('english')
    recognition = Recognition(speaker)
    brain = cells.get_brain()

    print('say something')
    while True:
        speech = recognition.listen_repeatdly()
        if speech:
            response = brain.respond(speech)

            if type(response) is str:
                speaker.speak(response)
            elif isinstance(response, ExecutableCellProxy):
                processable = response.forward(speaker, recognition)
                processable.process()
        else:
            print('empty speech')
    # response = listen()
    # understood = False
    # if response is not None:
    #     group = re.search(r'install\s(.+)', response)
    #     if group is not None:
    #         understood = True
    #         # speak(f'Do you want to install {group[1]}?')
    #         # response = listen()
    #         # if response is not None and 'yes' in response.lower():
    #         speak(f'Searching for {group[1]}')
    #         results = pexpect.run(f'dnf search --color=never {group[1]}')
    #         if b'No matches found' in results:
    #             speak(f'Anything found for {group[1]}')
    #         else:
    #             results = results.split(b'\n')
    #             results = list(filter(lambda s: not s.startswith(b'='), results))
    #             speak(f'{len(results)} results found')
    #             try:
    #                 package = SolutionFinder(results, show_max_results=2).find()
    #             except Exception as e:
    #                 print('failed to find')
    #                 print(f'{e.__class__.__name__}: {str(e)}')
    #     elif 'how are you' in response:
    #         understood = True
    #         speak('just doing my things, how about you?')
    #         response = listen()
    #         if response is not None:
    #             speak('awesome!')
    #
    # if understood is False and response is not None:
    #     speak(f'What is {response}?')

if __name__ == '__main__':
    main()
