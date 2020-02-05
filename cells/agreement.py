from .brain import IdentifiablePatternCell


def get_cell():
    return IdentifiablePatternCell(True, patterns=['yes', 'sure',
                    'of course', 'yep', 'no doubts', 'whitout a doubt', 'certainly',
                    'affirmative', 'fine', 'good', 'okay', 'yea', 'all right',
                    'definitely', 'sure thing', 'positive', 'nod bad'])
