from sbbbattlesim.spells import TargetedSpell
from sbbbattlesim.utils import StatChangeCause


class SpellType(TargetedSpell):
    display_name = 'Hugeify'

    def cast(self, target, *args, **kwargs):
        target.golden = True

    def filter(self, char):
        return not char.golden
