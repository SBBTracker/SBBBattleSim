from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Merlin's Test'''
    _level = 4
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
