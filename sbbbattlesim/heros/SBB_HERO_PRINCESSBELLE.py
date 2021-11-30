import random

from sbbbattlesim.events import OnDeath, OnSpellCast
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Beauty'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if Tribe.GOOD in target_character.tribes:
            target_character.tribes.add(Tribe.EVIL)
        elif Tribe.EVIL in target_character.tribes:
            target_character.tribes.add(Tribe.GOOD)
