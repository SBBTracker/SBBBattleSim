from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import random


class CharacterType(Character):
    display_name = 'Friendly Spirit'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.FriendlySpiritLastBreath)

    class FriendlySpiritLastBreath(OnDeath):
        def handle(self, dead_thing, *args, **kwargs):
            chars = self.manager.owner.valid_characters()
            if not chars:
                return

            attack_gift = 2*self.manager.attack if self.manager.golden else self.manager.attack
            health_gift = 2*self.manager.max_health if self.manager.golden else self.manager.max_health

            char = random.choice(chars)
            char.base_health += health_gift
            char.base_attack += attack_gift