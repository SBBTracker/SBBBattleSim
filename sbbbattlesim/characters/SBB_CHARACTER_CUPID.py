import logging

from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnPostDefend, OnPreAttack
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class CupidOnPostDefend(OnPostDefend):
    def __init__(self, *_args, **_kwargs):
        super().__init__(*_args, **_kwargs)
        self.used = False

    def handle(self, *_args, **_kwargs):
        if not self.used:
            if not self.manager.dead:
                attack(
                    attack_position=self.manager.position,
                    attacker=self.manager.player,
                    defender=self.manager.player
                )
                self.used = True


class CupidOnPreAttack(OnPreAttack):
    def handle(self, attack_position, defend_position, defend_player, *args, **kwargs):
        defend_character = defend_player.characters.get(defend_position)
        if defend_character is not None:
            defend_character.register(CupidOnPostDefend)


class CharacterType(Character):
    display_name = 'Cupid'

    _attack = 1
    _health = 10
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.FAIRY}

    flying = True
    ranged = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(CupidOnPreAttack)
