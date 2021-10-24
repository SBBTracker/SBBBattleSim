from sbbbattlesim.characters import Character
from sbbbattlesim.events import Slay


class CharacterType(Character):
    name = 'Brave Princess'

    class BravePrincessSlay(Slay):
        def __call__(self, **kwargs):
            pass

    events = (
        BravePrincessSlay,
    )
