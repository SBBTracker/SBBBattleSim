import random

from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Magic Research'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        target = random.choice(self.caster.valid_characters())
        target.change_stats(health=1, attack=1, temp=False, reason=f'{self} buff')