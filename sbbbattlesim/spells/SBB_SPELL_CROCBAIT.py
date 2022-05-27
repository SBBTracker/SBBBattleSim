from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Croc Bait'''
    _level = 6
    cost = 6

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
