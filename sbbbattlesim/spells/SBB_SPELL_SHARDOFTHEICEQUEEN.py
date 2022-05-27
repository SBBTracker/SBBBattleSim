from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''Shard of the Ice Queen'''
    _level = 2
    cost = 0
    targeted = True

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
