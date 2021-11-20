from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Humpty Dumpty'

    _attack = 7
    _health = 7
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.EGG}
    #TODO MAKE THIS DUMB MOTHERFUCKER DELETE ITSELF SO IT DOESN'T GET RESUMMONED BY PHEONIX FEATHER