from .brain import IdentifiablePatternCell, CellChoice
from . import agreement, disagreement, greetings, install, search, conversations


def get_brain(fallback_msg='I do not understand'):
    fallback = IdentifiablePatternCell(fallback_msg)

    return CellChoice([agreement.get_cell(), disagreement.get_cell(),
                     search.get_cell(), install.get_cell(), conversations.get_cell(),
                     greetings.get_cell()], fallback)


def get_binary_brain(default: bool):
    fallback = IdentifiablePatternCell(default)
    return CellChoice([agreement.get_cell(), disagreement.get_cell()], fallback)
