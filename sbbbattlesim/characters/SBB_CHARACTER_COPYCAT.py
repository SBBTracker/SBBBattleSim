import logging

from sbbbattlesim.action import ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPostAttack
from sbbbattlesim.utils import get_behind_targets, Tribe

logger = logging.getLogger(__name__)


class CopycatOnPostAttack(OnPostAttack):
    def handle(self, stack, *args, **kwargs):
        behind_targets = get_behind_targets(self.manager.position)
        targetted_chars = [c for c in self.manager.player.valid_characters() if c.position in behind_targets]

        itr = 2 if self.manager.golden else 1
        for _ in range(itr):
            with stack.open(source=self) as executor:
                for char in targetted_chars:
                    last_breaths = [evt for evt in char.get('OnDeath') if evt.last_breath]

                    for lb in last_breaths:
                        logger.debug(f'Copycat Triggering LastBreath({args} {kwargs})')
                        executor.execute(lb, reason=ActionReason.COPYCAT_PROC, *args, **kwargs)


class CharacterType(Character):
    display_name = 'Copycat'

    _attack = 2
    _health = 8
    _level = 4
    _tribes = {Tribe.ANIMAL, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(CopycatOnPostAttack, priority=100)
