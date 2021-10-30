from sbbbattlesim.characters import Character
from sbbbattlesim.events import Slay


class CharacterType(Character):
    name = 'Brave Princess'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.BravePrincessSlay)

    class BravePrincessSlay(Slay):
        def handle(self, *args, **kwargs):
            pass
