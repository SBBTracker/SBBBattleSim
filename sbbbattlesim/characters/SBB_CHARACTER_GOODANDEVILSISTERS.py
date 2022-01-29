import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class FairyBuffOnSummon(OnSummon):

    def handle(self, summoned_characters, stack, *args, **kwargs):
        if not self.source in summoned_characters:
            return

        highest_attack_evil = max([char.attack for char in self.source.player.valid_characters(
            _lambda=lambda char: Tribe.EVIL in char.tribes)] + [0])
        highest_health_good = max(
            [char.health for char in self.source.player.valid_characters() if Tribe.GOOD in char.tribes] + [0])
        multiplier = 2 if self.source.golden else 1
        # TODO: test coming out of wombats and croc
        Buff(reason=ActionReason.SHOULDER_FAIRY_BUFF, source=self.source, targets=[self.source],
             attack=highest_attack_evil * multiplier - (self.source.attack if highest_attack_evil > 0 else 0),
             health=highest_health_good * multiplier - (self.source.health if highest_health_good > 0 else 0),
             temp=False).resolve()


class CharacterType(Character):
    display_name = 'Shoulder Faeries'

    _attack = 1
    _health = 1
    _level = 5
    _tribes = {Tribe.FAIRY}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(FairyBuffOnSummon, source=self, priority=-16)

