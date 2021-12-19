from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Labyrinth Minotaur'
    aura = True

    _attack = 5
    _health = 1
    _level = 2
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, attack=2 if self.golden else 1,
                         _lambda=lambda char: Tribe.EVIL in char.tribes and char is not self)
