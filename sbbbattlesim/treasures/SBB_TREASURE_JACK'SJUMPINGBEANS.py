import random

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = '''Jack's Jumping Beans'''

    def __init__(self, player):
        super().__init__(player)

        class JacksJumpingBeansOnStartBuff(OnStart):
            def handle(self, *args, **kwargs):
                target_character = random.choice(self.manager.valid_characters())
                target_character.change_stats(attack=4, health=4, reason=214, source=self, temp=False)

        self.player.register(JacksJumpingBeansOnStartBuff)
