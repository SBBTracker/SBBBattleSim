from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill


class CharacterType(Character):
    display_name = 'Orge Princess'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.OgrePrincessSlay)

    class OgrePrincessSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            # TODO Summon random character or don't do this
            pass
