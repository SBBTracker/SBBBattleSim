from sbbbattlesim.utils import StatChangeCause, Tribe
from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnDeath
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Court Wizard'
    aura = True

    ranged = True

    _attack = 4
    _health = 2
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.MAGE}

    def buff(self, target_character, *args, **kwargs):
        if Tribe.PRINCESS in target_character.tribes or Tribe.PRINCE in target_character.tribes:

            class CourtWizardOnDeatheBuff(OnDeath):
                court_wizard = self
                last_breath = False

                def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
                    death_reason = next((stat_history_element.reason for stat_history_element in reversed(self.manager.stat_history) if stat_history_element.damage > 0))

                    if death_reason == StatChangeCause.DAMAGE_WHILE_DEFENDING:
                        attack(
                            attack_position=self.court_wizard.position,
                            attacker=self.manager.owner,
                            defender=self.manager.owner.opponent,
                            **kwargs
                        )

            target_character.register(CourtWizardOnDeatheBuff, temp=True)

