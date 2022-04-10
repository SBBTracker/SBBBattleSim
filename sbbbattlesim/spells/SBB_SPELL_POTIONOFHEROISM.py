from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Merlin's Test'''
    _level = 4
    cost = 3
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
