from sbbbattlesim.action import AuraBuff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Labyrinth Minotaur'
    aura = True

    _attack = 5
    _health = 1
    _level = 2
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def buff(self, target_character, *args, **kwargs):
        if Tribe.EVIL in target_character.tribes and target_character != self:
            AuraBuff(source=self, targets=[target_character], attack=2 if self.golden else 1, *args, **kwargs).resolve()
