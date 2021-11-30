from sbbbattlesim.characters import Character
import logging

from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Oni King'
    aura = True

    _attack = 13
    _health = 13
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def buff(self, target_character, *args, **kwargs):
        if Tribe.MONSTER in target_character.tribes:

            class OniKingOnMonsterAttack(OnPreAttack):
                oni_king = self
                def handle(self, stack, *args, **kwargs):
                    stat_change = 20 if self.oni_king.golden else 10
                    self.manager.change_stats(
                        attack=stat_change, health=stat_change, temp=False,
                        source=self.oni_king, reason=StatChangeCause.ONIKING_BUFF,
                        stack=stack
                    )

            target_character.register(OniKingOnMonsterAttack)
