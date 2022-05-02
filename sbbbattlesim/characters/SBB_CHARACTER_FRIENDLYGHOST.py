import random

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class FriendlySpiritLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        chars = self.manager.player.valid_characters(lambda char: char is not self.manager)
        if not chars:
            return

        golden_multiplyer = 2 if self.manager.golden else 1

        char = random.choice(chars)
        Buff(reason=ActionReason.FRIENDLY_SPIRIT_BUFF, source=self.manager, targets=[char],
             attack=self.manager.attack * golden_multiplyer, health=self.manager.max_health * golden_multiplyer,
             stack=stack).execute()


class CharacterType(Character):
    display_name = 'Friendly Spirit'
    last_breath = True

    _attack = 3
    _health = 4
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(FriendlySpiritLastBreath)
