from .brain import IdentifiablePatternCell


def get_cell():
    return IdentifiablePatternCell(responses=['Hello', 'Hi', 'Hey', 'Hi there'], patterns=['hi',
                    'hello', 'there you are', 'hey'])
