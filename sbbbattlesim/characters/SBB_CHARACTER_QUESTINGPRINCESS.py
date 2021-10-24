from sbbbattlesim.events import SlayEvent
from sbbbattlesim.characters import Character


class CharacterType(Character):
    name = 'Brave Princess'

    class BravePrincessSlay(SlayEvent):
        def __call__(self, **kwargs):
            pass

    slay = [
        BravePrincessSlay,
    ]


