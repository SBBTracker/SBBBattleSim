from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Turkish Delight'''
    _level = 3
    cost = 4

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
