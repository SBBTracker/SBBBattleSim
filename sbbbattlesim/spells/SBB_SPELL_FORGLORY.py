from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''For Glory!'''
    _level = 2
    cost = 1

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
