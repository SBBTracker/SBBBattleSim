from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Spinning Gold'''
    _level = 3

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
