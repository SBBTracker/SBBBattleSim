from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''The End'''
    _level = 4
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
