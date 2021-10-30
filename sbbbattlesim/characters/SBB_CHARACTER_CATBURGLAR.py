from sbbbattlesim.characters import Character
from sbbbattlesim.events import Slay


class CharacterType(Character):
    display_name = 'Kitty Cutpurse'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.KittyCutpurseSlay)

    class KittyCutpurseSlay(Slay):
        def handle(self, *args, **kwargs):
            pass
