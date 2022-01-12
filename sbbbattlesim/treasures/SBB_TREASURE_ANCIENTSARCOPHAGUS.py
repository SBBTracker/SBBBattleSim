import random

from sbbbattlesim.action import Damage, Aura, ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import Tribe


class AncientSarcophagusOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, reason, *args, **kwargs):
        for _ in range(self.source.mimic + 1):
            valid_targets = self.manager.player.opponent.valid_characters()
            if valid_targets:
                Damage(damage=3, reason=ActionReason.ANCIENT_SARCOPHAGUS, source=self.source,
                       targets=[random.choice(valid_targets)]).resolve()


class TreasureType(Treasure):
    display_name = 'Ancient Sarcophagus'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=AncientSarcophagusOnDeath, source=self,
                         _lambda=lambda char: Tribe.EVIL in char.tribes)
