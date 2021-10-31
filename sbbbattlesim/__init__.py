import enum

from sbbbattlesim.board import Board
from sbbbattlesim.config import configure_logging


class Tribes(enum.Enum):
    ANIMAL = 'animal'
    DRAGON = 'dragon'
    DWARF = 'dwarf'
    EGG = 'egg'
    FAIRY = 'fairy'
    MAGE = 'mage'
    MONSTER = 'monster'
    PRINCE = 'prince'
    PRINCESS = 'princess'
    PUFF_PUFF = 'puff puff'
    QUEEN = 'queen'
    Treant = 'treant'


class Keywords(enum.Enum):
    SUPPORT = 'support'
    FLYING = 'flying'
    SLAY = 'slay'
    LAST_BREATH = 'last breath'
    RANGED = 'ranged'
    QUEST = 'quest'

class DamageCause(enum.Enum):
    WHILE_ATTACKING = 1
    WHILE_DEFENDING = 2
    SPELL = 3


configure_logging()
