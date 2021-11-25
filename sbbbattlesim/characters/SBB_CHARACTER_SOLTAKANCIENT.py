import logging

from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import get_behind_targets, Tribe


logger = logging.getLogger(__name__)


class CharacterType(Character):
    display_name = 'Soltak Ancient'
    aura = True

    _attack = 0
    _health = 20
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def buff(self, target_character):
        behind = utils.get_behind_targets(self.position)
        if target_character.position in behind:
            logger.debug(f'{self.pretty_print()} is protecting {target_character.pretty_print()}')
            target_character.invincible = True
