from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Knighthood'
    _level = 6

    def cast(self, target, *args, **kwargs):
        target.golden = True
        # TODO base stats need to increase, i dont think it buffs echowood

    def filter(self, char):
        return not char.golden
