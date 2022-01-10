import logging

from sbbbattlesim import utils
from sbbbattlesim.action import Aura
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe
from sbbbattlesim.action import ActionState

logger = logging.getLogger(__name__)


class SoltakAuraBuff(Aura):
    def execute(self, *characters, **kwargs):
        logger.debug(f'{self} execute ({characters}, {kwargs})')
        for char in characters:
            if not self._lambda(char):
                continue

            self._char_buffer.add(char)
            char._action_history.append(self)

            logger.debug(f'{self.source.pretty_print()} is protecting {char.pretty_print()}')
            char.invincible = True

    def _clear(self, char, *args, **kwargs):
        logger.debug(f'{self.source.pretty_print()} is no longer protecting {char.pretty_print()}')
        char.invincible = False

    def roll_back(self, *characters, **kwargs):
        char_iter = characters or self._char_buffer.copy()
        logger.debug(f'{self} rolling back >>> {[char.pretty_print() for char in char_iter]}')
        for char in char_iter:
            if char not in self._char_buffer:
                continue
            self._char_buffer.remove(char)

            args = self.args
            kwargs = self.kwargs | kwargs

            self._clear(char, *args, **kwargs)

        self.state = ActionState.ROLLED_BACK



class CharacterType(Character):
    display_name = 'Soltak Ancient'
    aura = True

    _attack = 0
    _health = 20
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = SoltakAuraBuff(source=self, _lambda=lambda char: char.position in utils.get_behind_targets(self.position))
