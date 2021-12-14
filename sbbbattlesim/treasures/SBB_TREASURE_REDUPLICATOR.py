from sbbbattlesim.events import OnSummon
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.characters import registry as character_registry

class ReduplicatorOnSummon(OnSummon):
    def handle(self, summoned_characters, *args, **kwargs):
        if not self.reduplicator.triggered:
            if len(self.manager.valid_characters()) != 7:
                self.reduplicator.triggered = True
                for _ in range(self.reduplicator.mimic+1):
                    copied_character = summoned_characters[0]
                    new_character = character_registry[copied_character.id](
                        player=copied_character.player,
                        position=copied_character.position,
                        attack=copied_character._base_attack,
                        health=copied_character._base_health,
                        golden=copied_character.golden,
                        tribes=copied_character.tribes,
                        cost=copied_character.cost
                    )
                    self.manager.summon(new_character.position, [new_character], *args, **kwargs)


class TreasureType(Treasure):
    display_name = 'Reduplicator'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.player.register(ReduplicatorOnSummon, reduplicator=self, priority=-10)
