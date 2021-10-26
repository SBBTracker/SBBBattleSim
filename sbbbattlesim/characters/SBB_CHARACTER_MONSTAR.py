from sbbbattlesim.characters import Character
from sbbbattlesim.events import Slay


class CharacterType(Character):
    name = 'Orge Princess'

    class OgrePrincessSlay(Slay):
        def __call__(self, **kwargs):
            # TODO Summon random character or don't do this
            pass

    events = (
        OgrePrincessSlay,
    )
