from .brain import IdentifiablePatternCell


def get_cell():
    return IdentifiablePatternCell(False, patterns=['no', 'not', 'of course no',
                    'of course not', 'never', 'certainly not', 'no more',
                    'not at all', 'not either', 'negative', 'deny', 'refuse', 'reject',
                    'bad', 'not good'])
