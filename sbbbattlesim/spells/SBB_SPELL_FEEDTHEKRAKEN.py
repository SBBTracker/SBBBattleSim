from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Feed the Kraken'''
    _level = 4
    cost = 0
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
