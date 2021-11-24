from random import sample

from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = '''Toil and Trouble'''
    _level = 4

    def cast(self, player, *args, **kwargs):
        targets = sample(player.valid_characters(),2)
        for target in targets:
            target.change_stats(health=2, attack=2, temp=False, reason=StatChangeCause.WITCHS_BREW, source=self)

