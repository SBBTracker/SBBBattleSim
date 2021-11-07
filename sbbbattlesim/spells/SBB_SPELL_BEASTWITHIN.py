import random

from sbbbattlesim.events import OnDeath
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.characters import registry as character_registry


class SpellType(NonTargetedSpell):
    display_name = '''Cat's Call'''
    level = 0
    spell_filter = ()

    def cast(self, player, *args, **kwargs):
        class CatsCallOnDeath(OnDeath):
            def handle(self, *args, **kwargs):
                if not player.valid_characters(_lambda=lambda char: char.position in (1, 2, 3, 4)):
                    for pos in (1, 2, 3, 4):
                        player.summon(pos, character_registry['Cat'](self.manager.owner, self.manager.position, 1, 1, golden=False, keywords=[], tribes=['evil', 'animal'], cost=1))

        player.register(CatsCallOnDeath)
