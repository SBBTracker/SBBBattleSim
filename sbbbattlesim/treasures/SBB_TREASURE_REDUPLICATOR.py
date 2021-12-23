import logging

from sbbbattlesim.events import OnSummon
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.characters import registry as character_registry

logger = logging.getLogger(__name__)


class ReduplicatorOnSummon(OnSummon):
    def handle(self, summoned_characters, *args, **kwargs):
        if not self.source.triggered:
            if len(self.manager.valid_characters()) != 7:
                self.source.triggered = True
                for _ in range(self.source.mimic + 1):
                    copied_character = summoned_characters[0]
                    logger.debug(copied_character.pretty_print())
                    new_character = character_registry[copied_character.id](
                        player=copied_character.player,
                        position=copied_character.position,
                        attack=copied_character._base_attack,
                        health=copied_character._base_health,
                        golden=copied_character.golden,
                        tribes=copied_character.tribes,
                        cost=copied_character.cost
                    )
                    self.manager.summon(new_character.position, [new_character], raw=True, *args, **kwargs)


class TreasureType(Treasure):
    display_name = 'Reduplicator'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.player.register(ReduplicatorOnSummon, source=self, priority=-10)
