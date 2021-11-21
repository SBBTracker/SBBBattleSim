from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnSummon


class TreasureType(Treasure):
    display_name = 'Reduplicator'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

        class ReduplicatorOnSummon(OnSummon):
            reduplicator = self

            def handle(self, summoned_characters, *args, **kwargs):
                if not self.reduplicator.triggered:
                    if len(self.player.valid_characters()) != 7:
                        self.reduplicator.triggered = True
                        copied_character = summoned_characters[0]
                        new_character = copied_character.__class__.__init__(owner=copied_character.owner,
                                                                            position=copied_character.position,
                                                                            attack=copied_character.attack,
                                                                            health=copied_character.health,
                                                                            golden=copied_character.golden,
                                                                            tribes=copied_character.tribes,
                                                                            cost=copied_character.cost)
                        self.player.summon(new_character.position, new_character)

        self.player.register(ReduplicatorOnSummon)
