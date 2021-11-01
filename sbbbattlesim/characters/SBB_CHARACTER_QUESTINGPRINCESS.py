from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill


class CharacterType(Character):
    display_name = 'Brave Princess'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.BravePrincessSlay)

    class BravePrincessSlay(OnAttackAndKill):
        def handle(self, killed_character, *args, **kwargs):
            pass
