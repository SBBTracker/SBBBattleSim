import random

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = '''Jack's Jumping Beans'''

    _level = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class JacksJumpingBeansOnStartBuff(OnStart):
            beans = self
            def handle(self, stack, *args, **kwargs):
                for _ in range(self.beans.mimic + 1):
                    target_character = random.choice(self.beans.player.valid_characters())
                    target_character.change_stats(attack=4, health=4, reason=StatChangeCause.JACKS_JUMPING_BEANS, source=self.beans, temp=False, stack=stack)

        self.player.board.register(JacksJumpingBeansOnStartBuff)
