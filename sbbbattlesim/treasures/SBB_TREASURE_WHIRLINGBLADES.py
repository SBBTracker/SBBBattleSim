import logging

from sbbbattlesim.action import Buff, ActionReason, Aura, ActionState
from sbbbattlesim.events import OnBuff, OnSpawn, OnSummon
from sbbbattlesim.treasures import Treasure

logger = logging.getLogger(__name__)


class SingingSwordsAura(Aura):
    def __init__(self, *args, **kwargs):
        kwargs =  kwargs | dict(reason=ActionReason.SINGINGSWORD_BUFF)
        super().__init__(*args, **kwargs)
        self.multiplier = 3 if self.source.mimic else 2

    def execute(self, *characters, **kwargs):
        setup = kwargs.get('setup', False)
        from_copy = kwargs.get('from_copy', False)
        logger.debug(f'{self} execute ({characters}, {kwargs})')
        for char in characters or self.targets:
            if not self._lambda(char) or char in self._char_buffer:
                continue

            args = self.args
            kwargs = self.kwargs | kwargs
            self._char_buffer.add(char)
            char._action_history.append(self)

            # Custom Singing Sword Execute Logic
            # TODO If doubly implements multiplyers this needs to update
            logger.debug(f'Applying Singing Swords {char.pretty_print()}')

            starting_attack = char.attack
            char.attack_multiplier = self.multiplier
            if not setup or from_copy:
                char('OnBuff', reason=self.reason, source=self.source, attack=char.attack - starting_attack, health=0,
                     *args, **kwargs)
            else:
                char._base_attack = int(char._base_attack/char.attack_multiplier)

        self.state = ActionState.EXECUTED
        return self

    def _clear(self, char, *args, **kwargs):
        char._attack_multiplier = 1


class TreasureType(Treasure):
    display_name = 'Singing Swords'
    _level = 6
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = SingingSwordsAura(source=self, priority=999, _lambda=lambda char: char.position in (1, 2, 3, 4))
