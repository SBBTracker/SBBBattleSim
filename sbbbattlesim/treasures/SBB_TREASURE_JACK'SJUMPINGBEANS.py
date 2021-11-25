import random

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = '''Jack's Jumping Beans'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class JacksJumpingBeansOnStartBuff(OnStart):
            beans = self
            def handle(self, *args, **kwargs):
                for _ in range(self.beans.mimic + 1):
                    target_character = random.choice(self.manager.valid_characters())
                    target_character.change_stats(attack=4, health=4, reason=StatChangeCause.JACKS_JUMPING_BEANS, source=self.beans, temp=False)

        self.player.register(JacksJumpingBeansOnStartBuff)
