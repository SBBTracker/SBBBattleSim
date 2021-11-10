import random

from sbbbattlesim.events import OnDeath, OnSpellCast
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


MODRED_STR = 'SBB_HERO_MORDRED'

class HeroType(Hero):
    display_name = 'Merlin'
    aura = True

    def buff(self, target_character):

        class MordredOnDeath(OnDeath):
            def handle(self, *args, **kwargs):
                if self.manager.owner.stateful_effects.get(MODRED_STR, False):
                    return  # This has already procced
                self.manager.owner.stateful_effects[MODRED_STR] = True

                if self.manager.hand:
                    # TODO Fix logic on things with the same attack
                    high_attack_in_hand = sorted(self.manager.hand, key=lambda char: char.attack, reverse=True)[0]
                    self.manager.summon(high_attack_in_hand)

        target_character.register(MordredOnDeath)