from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Hi Ho!'''
    _level = 4
    cost = 3

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
