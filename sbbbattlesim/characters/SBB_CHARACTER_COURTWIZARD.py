import logging

from sbbbattlesim.action import AuraBuff, EventAura
from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause, Tribe

logger = logging.getLogger(__name__)


class CourtWizardOnDeathBuff(OnDeath):
    last_breath = False

    def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
        death_reason = next(
            (stat_history_element.reason for stat_history_element in reversed(self.manager._action_history) if
             stat_history_element.damage > 0))

        if death_reason == StatChangeCause.DAMAGE_WHILE_DEFENDING:
            attack(
                attack_position=self.court_wizard.position,
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
        self.aura_buff = EventAura(reason=StatChangeCause.AURA_BUFF, source=self, court_wizard=self,
                                   _lambda=lambda char: Tribe.PRINCESS in char.tribes or Tribe.PRINCE in char.tribes,
                                   event=CourtWizardOnDeathBuff)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
