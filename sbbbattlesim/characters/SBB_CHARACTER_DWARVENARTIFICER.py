from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon, OnStart, OnSpawn
from sbbbattlesim.utils import Tribe


class CraftyOnSpawn(OnSpawn):
    def handle(self, stack, *args, **kwargs):
        golden_multipler = 2 if self.source.golden else 1
        crafty_buff = 2 * len(self.source.player.treasures) * golden_multipler
        Buff(reason=ActionReason.CRAFTY_BUFF, source=self.source, targets=[self.source],
             attack=crafty_buff, health=crafty_buff, temp=True, *args, **kwargs).resolve()


class CharacterType(Character):
    display_name = 'Crafty'

    aura = True

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(CraftyOnSpawn)

    @classmethod
    def new(cls, player, position, golden):
        golden_multipler = 2 if golden else 1
        attack = cls._attack * golden_multipler
        health = cls._health * golden_multipler
        self = cls(
            player=player,
            position=position,
            golden=golden,
            attack=attack,
            health=health,
            tribes=cls._tribes,
            cost=cls._level
        )

        return self
