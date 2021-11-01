from sbbbattlesim.utils import StatChangeCause
from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnPreAttack, OnDamagedAndSurvived, OnDeath
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Cupid'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.CupidOnPreAttack)

    class CupidOnPreAttack(OnPreAttack):
        def handle(self, attack_character, defend_character, *args, **kwargs):

            class CupidConfusionOnDefendAndSurvive(OnDamagedAndSurvived):
                def handle(self, *args, **kwargs):
                    logger.debug(f'Cupid Confusion Is Causing an Attack')
                    attack(
                        attack_character=self.manager,
                        attacker=self.manager.owner,
                        defender=self.manager.owner
                    )
                    self.manager.unregister(self)

            defend_character.register(CupidConfusionOnDefendAndSurvive)

    class Bla(OnDeath):
        def handle(self, *args, **kwargs):
            return 'NotALastBreath', [], {}
