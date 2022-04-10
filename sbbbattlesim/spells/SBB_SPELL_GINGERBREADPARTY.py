from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Gingerbread Party'''
    _level = 3
    cost = 3

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
