import random

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.spells import NonTargetedSpell

PIGOMORPH_ID = 'SBB_CHARACTER_PIG'


class SpellType(NonTargetedSpell):
    display_name = 'Pigomorph'
    _level = 6

    def cast(self, player, *args, **kwargs):
        target = random.choice(player.opponent.valid_characters())
        if target is not None:
            pig = character_registry[PIGOMORPH_ID](player.opponent, target.position, 10, 10, golden=False, keywords=[], tribes=[], cost=1)
            player.characters[target.position] = pig
            player.opponent.resolve_board()
