from sbbbattlesim.utils import StatChangeCause
from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnDamagedAndSurvived, OnDeath, OnPostAttack
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Cupid'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.CupidOnPreAttack)

    class CupidOnPreAttack(OnPostAttack):
        def handle(self, attack_position, defend_position, *args, **kwargs):

            defend_character = self.manager.owner.opponent.characters.get(defend_position)
            if defend_character is not None:
                if not defend_character.dead:

                    opponent = self.manager.owner.opponent

                    attack(
                        attack_position=defend_position,
                        attacker=opponent,
                        defender=opponent
                    )

    class Bla(OnDeath):
        def handle(self, *args, **kwargs):
            return 'NotALastBreath', [], {}
