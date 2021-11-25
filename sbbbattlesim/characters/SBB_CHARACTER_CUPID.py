from sbbbattlesim.utils import StatChangeCause, Tribe
from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnDamagedAndSurvived, OnDeath, OnPostDefend, OnPreAttack

import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Cupid'

    _attack = 1
    _health = 10
    _level = 5
    _tribes = {Tribe.GOOD, Tribe.FAIRY}

    flying = True
    ranged = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.CupidOnPreAttack)

    class CupidOnPreAttack(OnPreAttack):

        def handle(self, attack_position, defend_position, defend_player, *args, **kwargs):

            class CupidOnPostDefend(OnPostDefend):
                def __init__(self, *_args, **_kwargs):
                    super().__init__(*_args, **_kwargs)
                    self.used = False

                def handle(self, *_args, **_kwargs):

                    if not self.used:
                        if not self.manager.dead:
                            attack(
                                attack_position=self.manager.position,
                                attacker=self.manager.owner,
                                defender=self.manager.owner
                            )
                            self.used = True

            defend_character = defend_player.characters.get(defend_position)
            if defend_character is not None:
                defend_character.register(CupidOnPostDefend)