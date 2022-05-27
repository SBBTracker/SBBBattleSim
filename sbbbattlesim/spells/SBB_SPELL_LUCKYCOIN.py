from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Lucky Coin'''
    _level = 5
    cost = 0
    cantrip = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
