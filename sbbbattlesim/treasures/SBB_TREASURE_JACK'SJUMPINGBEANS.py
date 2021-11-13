from random import choice

from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = '''Jack's Jumping Beans'''

    def __init__(self, player):
        super().__init__(player)

        class JacksJumpingBeansOnStartBuff(OnStart):
            def handle(self, *args, **kwargs):
                target_character = choice(self.manager.valid_characters())
                target_character.change_stats(attack=4, health=4, reason=StatChangeCause.JACKS_JUMPING_BEANS,
                                              source=self, temp=False)

        self.player.register(JacksJumpingBeansOnStartBuff)