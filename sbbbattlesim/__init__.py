import logging

from sbbbattlesim.board import Board
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.player import Player
from sbbbattlesim.treasures import registry as treasure_registry

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


formatter = logging.Formatter('%(asctime)-15s %(name)-25s %(funcName)-20s %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
for logger_name in ['sbbbattlesim.characters', 'sbbbattlesim.heros', 'sbbbattlesim.treasures', 'sbbbattlesim.combat', 'sbbbattlesim.events', 'sbbbattlesim.player']:
    logger = logging.getLogger(logger_name)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)

# __all__ = [
#     character_registry, hero_registry, treasure_registry,
#     Player, Board, keywords, tribes
# ]
