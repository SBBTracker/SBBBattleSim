from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Kitty Cutpurse'
    slay = True

    _attack = 1
    _health = 1
    _level = 2
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.KittyCutpurseSlay)

    class KittyCutpurseSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            pass
