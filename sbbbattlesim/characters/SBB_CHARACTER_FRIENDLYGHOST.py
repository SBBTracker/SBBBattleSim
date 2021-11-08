from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import random

from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Friendly Spirit'
    last_breath = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.FriendlySpiritLastBreath)

    class FriendlySpiritLastBreath(OnDeath):
        last_breath = True
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
                reason=StatChangeCause.FRIENDLY_SPIRIT_BUFF,
                source=self.manager
            )