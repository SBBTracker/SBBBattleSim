from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnPreAttack

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Oni King'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def buff(self, target_character):
        if 'monster' in target_character.tribes:

            class OniKingOnMonsterAttack(OnPreAttack):
                oni_king = self
                def handle(self, *args, **kwargs):
                    stat_change = 20 if self.oni_king.golden else 10
                    self.manager.change_stats(attack=stat_change, health=stat_change, temp=False, reason=f'{self.oni_king} on attack buff')

            target_character.register(OniKingOnMonsterAttack)