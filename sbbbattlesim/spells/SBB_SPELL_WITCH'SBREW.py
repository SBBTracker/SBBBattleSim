from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = '''Witch's Brew'''
    _level = 2

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=1, attack=1, temp=False, reason=StatChangeCause.WITCHS_BREW, source=self, stack=None)

    def filter(self, char):
        return Tribe.EVIL in char.tribes