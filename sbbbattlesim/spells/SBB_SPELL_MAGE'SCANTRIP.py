from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Healing Potion'''
    _level = 3
    cost = 1
    cantrip = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
