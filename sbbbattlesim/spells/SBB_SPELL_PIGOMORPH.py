import random

from sbbbattlesim.spells import NonTargetedSpell
from sbbbattlesim.characters import registry as character_registry


PIGOMORPH_ID = 'SBB_CHARACTER_PIG'


class SpellType(NonTargetedSpell):
    display_name = 'Pigomorph'

    def cast(self, player, *args, **kwargs):
        target = random.choice(player.opponent.valid_characters())
        if target is not None:
            pig = character_registry[PIGOMORPH_ID](player.opponent, target.position, 10, 10, golden=False, keywords=[], tribes=[], cost=1)
            player.characters[target.position] = pig
            player.opponent.resolve_board()
