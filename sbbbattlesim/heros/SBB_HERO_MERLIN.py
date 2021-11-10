import random

from sbbbattlesim.events import OnDeath, OnSpellCast
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Merlin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class MerlinOnSpellCast(OnSpellCast):
            merlin = self
            def handle(self, caster, spell, target, *args, **kwargs):
                valid_characters = self.manager.valid_characters()
                if valid_characters:
                    target_character = random.choice(valid_characters)
                    target_character.change_stats(attack=2, health=1, reason=StatChangeCause.MERLIN_BUFF, source=self.merlin)

        self.player.register(MerlinOnSpellCast)