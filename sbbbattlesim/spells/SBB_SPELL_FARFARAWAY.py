from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''The End'''
    _level = 4
    cost = 3
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
