import random

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.spells import Spell
from sbbbattlesim.utils import Tribe

PIGOMORPH_ID = 'SBB_CHARACTER_PIG'


class SpellType(Spell):
    display_name = 'Pigomorph'
    _level = 6
    cost = 5

    def cast(self, target: 'Character' = None, *args, **kwargs):
        valid_targets = self.player.opponent.valid_characters(lambda char: char.id not in [PIGOMORPH_ID])
        if valid_targets:
            target = random.choice(valid_targets)
            pig = character_registry[PIGOMORPH_ID](
                target.player, target.position, 10, 10, golden=False,
                keywords=[], tribes=[Tribe.ANIMAL], cost=1
            )
            target.player.transform(target.position, pig)
