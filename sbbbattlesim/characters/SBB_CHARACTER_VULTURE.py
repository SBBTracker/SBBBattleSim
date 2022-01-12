import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class BeardedVultureOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, reason, *args, **kwargs):
        stat_change = 6 if self.source.golden else 3
        Buff(source=self.source, reason=ActionReason.BEARDEDVULTURE_BUFF, targets=[self.source],
             attack=stat_change, health=stat_change, temp=False).resolve()


class CharacterType(Character):
    display_name = 'Bearded Vulture'
    aura = True

    _attack = 3
    _health = 3
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, event=BeardedVultureOnDeath,
                         _lambda=lambda char: Tribe.ANIMAL in char.tribes and char is not self)
