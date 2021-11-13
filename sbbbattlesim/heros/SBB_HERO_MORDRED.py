import random

from sbbbattlesim.events import OnDeath, OnSpellCast
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


MODRED_STR = 'SBB_HERO_MORDRED'

class HeroType(Hero):
    display_name = MODRED_STR
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

    def buff(self, target_character):
        class MordredOnDeath(OnDeath):
            modred = self
            last_breath = False
            def handle(self, *args, **kwargs):
                if self.modred.triggered:
                    return  # This has already procced
                self.modred.triggered = True

                if self.manager.owner.hand:
                    high_attack_in_hand = sorted(self.manager.owner.hand, key=lambda char: char.attack, reverse=True)[0]
                    self.manager.owner.summon(self.manager.position, high_attack_in_hand)

        target_character.register(MordredOnDeath, temp=True)