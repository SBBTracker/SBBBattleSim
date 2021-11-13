import random

from sbbbattlesim.events import OnDeath, OnSpellCast
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Potion Master'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class PotionMasterOnSpellCast(OnSpellCast):
            potion_master = self
            def handle(self, caster, spell, target, *args, **kwargs):
                if target is not None:
                    target.change_stats(attack=2, health=2, reason=StatChangeCause.POTION_MASTER_BUFF, source=self.potion_master, temp=False)

        self.player.register(PotionMasterOnSpellCast)