import random

from sbbbattlesim.action import Damage, EventAura
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause, Tribe


class AncientSarcophagusOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        for _ in range(self.ancient_sarcophagus.mimic + 1):
            valid_targets = self.manager.player.opponent.valid_characters()
            if valid_targets:
                Damage(damage=3, reason=StatChangeCause.ANCIENT_SARCOPHAGUS, source=self.ancient_sarcophagus,
                       targets=[random.choice(valid_targets)]).resolve()


class TreasureType(Treasure):
    display_name = 'Ancient Sarcophagus'
    aura = True

    _level = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = EventAura(event=AncientSarcophagusOnDeath, source=self, ancient_sarcophagus=self,
                                   _lambda=lambda char: Tribe.EVIL in char.tribes)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
