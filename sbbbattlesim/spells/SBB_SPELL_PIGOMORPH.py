import random

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.utils import Tribe

PIGOMORPH_ID = 'SBB_CHARACTER_PIG'


class SpellType(NonTargetedSpell):
    display_name = 'Pigomorph'
    _level = 6

    def cast(self, player, *args, **kwargs):
        valid_targets = player.opponent.valid_characters()
        if valid_targets:
            target = random.choice(valid_targets)
            pig = character_registry[PIGOMORPH_ID](
                target.owner, target.position, 10, 10, golden=False,
                keywords=[], tribes=[Tribe.ANIMAL], cost=1
            )
            target.owner.characters[target.position] = pig
            target.owner.opponent.resolve_board()
