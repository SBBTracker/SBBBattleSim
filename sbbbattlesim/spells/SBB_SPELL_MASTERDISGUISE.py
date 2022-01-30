from sbbbattlesim.spells import Spell


class SpellType(Spell):
    display_name = '''It Was All a Dream'''
    _level = 6

    def cast(self, target: 'Character' = None, *args, **kwargs):
        pass
