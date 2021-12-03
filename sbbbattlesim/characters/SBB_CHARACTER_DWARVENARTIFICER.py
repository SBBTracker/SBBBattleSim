from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Crafty'

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.DWARF}

    def new(cls, owner, position, golden):
        golden_multipler = 2 if golden else 1
        attack = (cls._attack + (3 * owner.treasures)) * golden_multipler
        health = (cls._health + (3 * owner.treasures)) * golden_multipler

        return cls(
            owner=owner,
            position=position,
            golden=golden,
            attack=attack,
            health=health,
            tribes=cls._tribes,
            cost=cls._level
        )
