from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Drink Me Potion'''
    _level = 6
    cost = 1
    cantrip = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
