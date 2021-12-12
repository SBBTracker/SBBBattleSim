import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)


class HungryHungryHippocampusOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        _lambda = lambda char: Tribe.ANIMAL in char.tribes and char is not self.hippo
        num_animals = len(list(filter(_lambda, summoned_characters)))
        modifier = 4 if self.hippo.golden else 2

        if self.hippo in self.manager.characters.values():
            Buff(source=self.hippo, reason=StatChangeCause.HUNGRYHUNGRYHIPPOCAMPUS_BUFF, targets=[self.hippo],
                 health=num_animals * modifier, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Hungry Hungry Hippocampus'

    aura = True

    _attack = 10
    _health = 1
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def buff(self, target_character, *args, **kwargs):
        if target_character is self:
            self.player.register(HungryHungryHippocampusOnSummon, temp=True, hippo=self)
