from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon
from sbbbattlesim.utils import StatChangeCause, Tribe


class CraftyOnSummon(OnSummon):

    def handle(self, summoned_characters, stack, *args, **kwargs):
        golden_multipler = 2 if self.crafty.golden else 1
        crafty_buff = 3 * len(self.manager.treasures) * golden_multipler
        self.crafty.change_stats(attack=crafty_buff, health=crafty_buff, temp=False,
                                 reason=StatChangeCause.CRAFTY_BUFF, source=self)


# NOTE: crafty does not work without raw=true for being on the default board with treasures
# this may be common with other calculated effects
class CharacterType(Character):
    display_name = 'Crafty'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner.register(CraftyOnSummon, crafty=self)

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
