from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import Tribe


class SpellType(TargetedSpell):
    display_name = '''Witch's Brew'''
    _level = 2

    def cast(self, target, *args, **kwargs):
        Buff(health=1, attack=1, temp=False, reason=ActionReason.WITCHS_BREW, source=self, *args, **kwargs)

    def filter(self, char):
        return Tribe.EVIL in char.tribes
