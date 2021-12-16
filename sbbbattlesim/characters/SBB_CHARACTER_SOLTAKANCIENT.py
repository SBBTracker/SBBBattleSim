import logging

from sbbbattlesim import utils
from sbbbattlesim.action import Aura
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class SoltakAuraBuff(Aura):
    def _apply(self, char, *args, **kwargs):
        logger.debug(f'{self.source.pretty_print()} is protecting {char.pretty_print()}')
        char.invincible = True


class CharacterType(Character):
    display_name = 'Soltak Ancient'
    aura = True

    _attack = 0
    _health = 20
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = SoltakAuraBuff(source=self, _lambda=lambda char: char.position in utils.get_behind_targets(self.position))

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
