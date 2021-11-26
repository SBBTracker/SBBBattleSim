import random

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause, Tribe
from sbbbattlesim.characters import registry as character_registry


class CharacterType(Character):
    display_name = 'Great Pumpkin King'

    _attack = 5
    _health = 5
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class PumpkinKingOnDeath(OnDeath):
            def handle(self, *args, **kwargs):
                summons = []
                dead_in_order = sorted(
                    [char for char in self.manager.graveyard if Tribe.EVIL in char],
                    key=lambda char: char._level, reverse=True
                )
                for dead in dead_in_order[:7]:
                    summon_choices = character_registry.get(
                        _lambda=lambda char: char._level == dead._level-1 and Tribe.EVIL in char._tribes
                    )
                    if summon_choices:
                        summons.append(random.choice(summon_choices).new(
                            owner=self.manager.owner,
                            position=self.manager.position,
                            golden=self.manager.golden
                        ))

                self.manager.owner.summon(self.manager.position, *summons)