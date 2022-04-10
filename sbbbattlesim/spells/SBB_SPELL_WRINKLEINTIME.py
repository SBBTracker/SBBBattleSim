from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Mixawizzle'''
    _level = 3
    cost = 1
    targeted = True
    cantrip = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
