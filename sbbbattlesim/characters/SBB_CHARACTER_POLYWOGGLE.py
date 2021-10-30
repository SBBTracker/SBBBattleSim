from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay


class CharacterType(Character):
    display_name = 'Polywoggle'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.PolywoggleSlay)

    class PolywoggleSlay(OnSlay):
        def handle(self, *args, **kwargs):
            pass  #TODO implement random spawn on survive
