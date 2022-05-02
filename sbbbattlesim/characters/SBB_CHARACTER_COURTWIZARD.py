import logging

from sbbbattlesim.action import Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class CourtWizardOnDeathBuff(OnDeath):
    last_breath = False

    def handle(self, stack, reason=None, *args, **kwargs):
        if reason:
            if reason == ActionReason.DAMAGE_WHILE_ATTACKING:
                attack(
                    attack_position=self.source.position,
                    attacker=self.manager.player,
                    defender=self.manager.player.opponent,
                    **kwargs
                )


class CharacterType(Character):
    display_name = 'Court Wizard'
    aura = True

    ranged = True

    _attack = 4
    _health = 2
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(event=CourtWizardOnDeathBuff, reason=ActionReason.AURA_BUFF, source=self, priority=90,
                         _lambda=lambda char: Tribe.ROYAL in char.tribes)
