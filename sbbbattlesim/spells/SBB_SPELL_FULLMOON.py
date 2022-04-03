from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Potion of Heroism'''
    _level = 3
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
