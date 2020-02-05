from .brain import IdentifiablePatternCell


def get_cell():
    return IdentifiablePatternCell(responses=['running like a charm', 'just fine',
                'just doing my things', 'working hard as always'],
                patterns=['how are you', 'what have you been doing', 'how you doing',
                'what\'s up'])
