from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause, Tribe


class SpellType(TargetedSpell):
    display_name = '''Beauty's Influence'''
    _level = 3

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=3, attack=3, temp=False, reason=StatChangeCause.BEAUTYS_INFLUENCE, source=self, stack=None)

        target.tribes.remove(Tribe.EVIL)
        target.tribes.add(Tribe.GOOD)

    def filter(self, char):
        return Tribe.EVIL in char.tribes