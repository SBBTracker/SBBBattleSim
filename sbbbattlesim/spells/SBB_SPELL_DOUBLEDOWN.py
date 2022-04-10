from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Spinning Gold'''
    _level = 3
    cost = 1

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
