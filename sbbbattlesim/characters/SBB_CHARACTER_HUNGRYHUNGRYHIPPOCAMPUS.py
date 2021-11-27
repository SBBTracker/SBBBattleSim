import logging

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Hungry Hungry Hippocampus'

    aura = True

    _attack = 10
    _health = 1
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def buff(self, target_character, *args, **kwargs):
        class HungryHungryHippocampusOnSummon(OnSummon):
            hungry_hungry_hippocampus = self

            def handle(self, summoned_characters, *args, **kwargs):
                num_animals = len(list(filter(lambda char: Tribe.ANIMAL in char.tribes, summoned_characters)))
                modifier = 4 if self.hungry_hungry_hippocampus.golden else 2

                if self.hungry_hungry_hippocampus in self.manager.characters.values():
                    self.hungry_hungry_hippocampus.change_stats(
                        health=num_animals*modifier,
                        temp=False,
                        source=self.hungry_hungry_hippocampus,
                        reason=StatChangeCause.HUNGRYHUNGRYHIPPOCAMPUS_BUFF
                    )

        if target_character is self:
            self.owner.register(HungryHungryHippocampusOnSummon, temp=True)
