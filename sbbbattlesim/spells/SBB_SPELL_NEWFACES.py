from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Masquerade Ball'''
    _level = 4
    cost = 2

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
