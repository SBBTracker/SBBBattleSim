from sbbbattlesim.utils import Tribe

from sbbbattlesim.characters import Character


class CharacterType(Character):
    display_name = 'Gingerbread Knight'

    _attack = 7
    _health = 7
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.ROYAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: check hero health for buff