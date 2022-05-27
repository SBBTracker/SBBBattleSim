from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Kidnap'''
    _level = 3
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
