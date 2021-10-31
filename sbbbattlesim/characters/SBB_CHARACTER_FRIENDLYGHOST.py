from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import random


class CharacterType(Character):
    display_name = 'Friendly Spirit'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.FriendlySpiritLastBreath)

    class FriendlySpiritLastBreath(OnDeath):
        def handle(self, *args, **kwargs):
            chars = self.manager.owner.valid_characters()
            if not chars:
                return

            golden_multiplyer = 2 if self.manager.golden else 1

            char = random.choice(chars)
            char.change_stats(
                attack=self.manager.attack * golden_multiplyer,
                health=self.manager.max_health * golden_multiplyer,
                temp=False,
                reason=f'Friendly spirit buff from {self}'
            )