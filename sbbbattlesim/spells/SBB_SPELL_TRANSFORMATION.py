from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''True Love's Kiss'''
    _level = 3
    cost = 3
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
