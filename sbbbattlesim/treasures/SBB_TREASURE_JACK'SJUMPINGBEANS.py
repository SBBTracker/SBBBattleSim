import random

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class JacksJumpingBeansOnStartBuff(OnStart):
    def handle(self, stack, *args, **kwargs):
        for _ in range(self.source.mimic + 1):
            target_character = random.choice(self.source.player.valid_characters())
            Buff(reason=ActionReason.JACKS_JUMPING_BEANS, source=self.source, targets=[target_character],
                 attack=4, health=4, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = '''Jack's Jumping Beans'''

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(JacksJumpingBeansOnStartBuff, source=self)
