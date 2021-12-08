import random

from sbbbattlesim.action import Buff
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class JacksJumpingBeansOnStartBuff(OnStart):
    def handle(self, stack, *args, **kwargs):
        for _ in range(self.beans.mimic + 1):
            target_character = random.choice(self.beans.player.valid_characters())
            Buff(reason=StatChangeCause.JACKS_JUMPING_BEANS, source=self.beans, targets=[target_character],
                 attack=4, health=4,  temp=False, stack=stack).resolve()


class TreasureType(Treasure):
    display_name = '''Jack's Jumping Beans'''

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.board.register(JacksJumpingBeansOnStartBuff, beans=self)
