from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Shrink Spell'''
    _level = 2
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
