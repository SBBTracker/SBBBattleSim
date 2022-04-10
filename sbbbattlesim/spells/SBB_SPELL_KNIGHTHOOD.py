from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = 'Knighthood'
    _level = 6
    cost = 12
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        target.golden = True
        # TODO base stats need to increase, i dont think it buffs echowood

    @classmethod
    def filter(cls, char):
        return not char.golden
