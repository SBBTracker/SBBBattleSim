from sbbbattlesim.utils import StatChangeCause
from sbbbattlesim.characters import Character
from sbbbattlesim.combat import attack
from sbbbattlesim.events import OnDeath
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Court Wizard'
    aura = True

    def buff(self, target_character):
        if 'princess' in target_character.tribes or 'prince' in target_character.tribes:

            class CourtWizardOnDeatheBuff(OnDeath):
                court_wizard = self
                def handle(self, attack_buff=0, health_buff=0, temp=False, *args, **kwargs):
                    death_reason = next(reason for (reason, _, _, damage, _, _) in reversed(self.manager.stat_history) if damage > 0)
                    if death_reason == StatChangeCause.DAMAGE_WHILE_DEFENDING:
                        attack(
                            attack_character=self.court_wizard,
                            attacker=self.manager.owner,
                            defender=self.manager.owner.opponent,
                            **kwargs
                        )

            target_character.register(CourtWizardOnDeatheBuff, temp=True)

