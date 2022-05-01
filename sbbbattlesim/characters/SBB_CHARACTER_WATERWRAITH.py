import logging

from sbbbattlesim.action import Buff, Action, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class WaterWraithOnSummon(OnSummon):
    def handle(self, summoned_characters, stack, *args, **kwargs):
        _lambda = lambda char: char.slot and char is not self.source # how do I check adjacency
        num_chars = len(list(filter(_lambda, summoned_characters)))
        modifier = 2 if self.source.golden else 1

        if self.source in self.manager.characters.values():
            Buff(source=self.source, reason=ActionReason.WATER_WRAITH_BUFF, targets=[self.source],
                 health=num_chars * modifier, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Water Wraith'

    _attack = 2
    _health = 2
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(WaterWraithOnSummon, source=self)
