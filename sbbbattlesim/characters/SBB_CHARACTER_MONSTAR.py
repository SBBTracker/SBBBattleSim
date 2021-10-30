from sbbbattlesim.characters import Character
from sbbbattlesim.events import Slay


class CharacterType(Character):
    display_name = 'Orge Princess'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.OgrePrincessSlay)

    class OgrePrincessSlay(Slay):
        def __call__(self, **kwargs):
            # TODO Summon random character or don't do this
            pass
