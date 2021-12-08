from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon, OnStart
from sbbbattlesim.utils import StatChangeCause, Tribe



class CharacterType(Character):
    display_name = 'Crafty'

    aura = True

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def buff(self, target_character, *args, **kwargs):
        if target_character is self:
            golden_multipler = 2 if self.golden else 1
            crafty_buff = 3 * len(self.owner.treasures) * golden_multipler
            with Buff(reason=StatChangeCause.CRAFTY_BUFF, source=self, targets=[self],
                      attack=crafty_buff, health=crafty_buff, temp=True, *args, **kwargs):
                pass

    @classmethod
    def new(cls, owner, position, golden):
        golden_multipler = 2 if golden else 1
        attack = cls._attack * golden_multipler
        health = cls._health * golden_multipler

        self = cls(
            owner=owner,
            position=position,
            golden=golden,
            attack=attack,
            health=health,
            tribes=cls._tribes,
            cost=cls._level
        )

        return self
