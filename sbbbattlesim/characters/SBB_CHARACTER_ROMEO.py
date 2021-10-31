from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import sbbbattlesim
from sbbbattlesim.characters import registry as character_registry

import random

JULIET_ID = 'SBB_CHARACTER_JULIET'

class CharacterType(Character):
    display_name = 'Romeo'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.RomeoLastBreath)

    class RomeoLastBreath(OnDeath):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            juliet = max([j for j in self.manager.owner.graveyard if j.id == JULIET_ID],
                         key=lambda juliet : (juliet.attack, juliet.health)
                         )
            juliet._damage = 0  # Reset damage dealt to this unit

            # QUESTION Does juliet pick the biggest attack & health one or does it sort on golden as well
            modifier = 14 if self.manager.golden else 7
            j_attack, j_health = juliet.attack + modifier, juliet.health + modifier

            juliets = [character_registry[JULIET_ID](self.manager.owner, self.manager.position, j_attack, j_health,
                                                  golden=juliet.golden, keywords=[], tribes=['good', 'princess'],
                                                  cost=juliet.cost)]

            self.manager.owner.summon(self.manager.position, *juliets)
