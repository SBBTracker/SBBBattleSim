from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe, StatChangeCause
from sbbbattlesim.action import AuraBuff

class CharacterType(Character):
    display_name = 'Princess Wight'
    aura = True
    quest = True

    _attack = 2
    _health = 4
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.PRINCESS}

    def buff(self, target_character, *args, **kwargs):
        if Tribe.DWARF in target_character.tribes:
            modifier = 2 if self.golden else 1
            AuraBuff(source=self, targets=[target_character],
                     attack=modifier, health=modifier, *args, **kwargs).resolve()
