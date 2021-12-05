import logging

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)

STATUE_ID = 'SBB_CHARACTER_STATUE'

class CharacterType(Character):
    display_name = 'Medusa'

    _attack = 3
    _health = 3
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.MedusaOnPreAttack)

    class MedusaOnPreAttack(OnPreAttack):
        def handle(self, defend_position, *args, **kwargs):
            attack = 0
            health = 3 if self.manager.golden else 6

            defend_character = self.manager.owner.opponent.characters[defend_position]

            if defend_character.id != STATUE_ID:
                new_statue = character_registry[STATUE_ID](
                    self.manager.owner,
                    defend_character.position,
                    attack,
                    health,
                    golden=False,
                    keywords=[], tribes=[], cost=1
                )
                defend_character.owner.characters[defend_character.position] = new_statue
                defend_character.owner.resolve_board()






