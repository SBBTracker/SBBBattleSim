import random

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause, Tribe


class FriendlySpiritLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, *args, **kwargs):
        chars = self.manager.owner.valid_characters()
        if not chars:
            return

        golden_multiplyer = 2 if self.manager.golden else 1

        char = random.choice(chars)
        with Buff(reason=StatChangeCause.FRIENDLY_SPIRIT_BUFF, source=self.manager, targets=[char],
                  attack=self.manager.attack * golden_multiplyer, health=self.manager.max_health * golden_multiplyer,
                  temp=False, stack=stack):
            pass


class CharacterType(Character):
    display_name = 'Friendly Spirit'
    last_breath = True

    _attack = 3
    _health = 3
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(FriendlySpiritLastBreath)
