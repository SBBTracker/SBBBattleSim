from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Forbidden Fruit'''
    _level = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
