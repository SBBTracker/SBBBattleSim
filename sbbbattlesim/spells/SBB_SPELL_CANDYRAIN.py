from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Candy Rain'''
    _level = 3
    cost = 0

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
