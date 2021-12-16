import logging

from sbbbattlesim.action import Buff, Action, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class HungryHungryHippocampusOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        _lambda = lambda char: Tribe.ANIMAL in char.tribes and char is not self.hippo
        num_animals = len(list(filter(_lambda, summoned_characters)))
        modifier = 4 if self.hippo.golden else 2

        if self.hippo in self.manager.characters.values():
            Buff(source=self.hippo, reason=ActionReason.HUNGRYHUNGRYHIPPOCAMPUS_BUFF, targets=[self.hippo],
                 health=num_animals * modifier, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Hungry Hungry Hippocampus'

    _attack = 10
    _health = 1
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_buff = Action(source=self, event=HungryHungryHippocampusOnSummon, hippo=self, reason=ActionReason.HUNGRYHUNGRYHIPPOCAMPUS_BUFF)
