from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Knighthood'
    _level = 6

    def cast(self, target, *args, **kwargs):
        target.golden = True

    def filter(self, char):
        return not char.golden
