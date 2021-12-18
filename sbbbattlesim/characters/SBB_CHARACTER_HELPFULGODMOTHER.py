from sbbbattlesim.action import Buff, Aura, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Rainbow Unicorn'
    aura = True

    _attack = 1
    _health = 5
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, health=2 if self.golden else 1,
                              _lambda=lambda char: Tribe.GOOD in char.tribes and char is not self)

    
