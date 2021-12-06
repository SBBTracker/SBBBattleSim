from sbbbattlesim.events import OnSummon
from sbbbattlesim.treasures import Treasure


class ReduplicatorOnSummon(OnSummon):

    def handle(self, summoned_characters, *args, **kwargs):
        if not self.reduplicator.triggered:
            if len(self.manager.valid_characters()) != 7:
                self.reduplicator.triggered = True
                copied_character = summoned_characters[0]
                new_character = copied_character.__class__.__init__(
                    owner=copied_character.owner,
                    position=copied_character.position,
                    attack=copied_character.attack,
                    health=copied_character.health,
                    golden=copied_character.golden,
                    tribes=copied_character.tribes,
                    cost=copied_character.cost
                )
                self.manager.summon(new_character.position, [new_character])


class TreasureType(Treasure):
    display_name = 'Reduplicator'

    _level = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False
        self.player.register(ReduplicatorOnSummon, reduplicator=self)
