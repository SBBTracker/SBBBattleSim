from sbbbattlesim.board import Board
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.player import Player

keywords = (
    'support',
    'flying',
    'slay',
    'last breath',
    'ranged',
    'quest',
)

tribes = (
    'animal',
    'monster',
    'mage',
    'princess',
    'prince',
    'queen',
    'dwarf',
    'fairy',
    'puff puff',
    'dragon',
    
    'good',
    'evil'
)


__all__ = [
    character_registry, hero_registry, treasure_registry,
    Player, Board, keywords, tribes
]


