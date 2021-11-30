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
            target_character.change_stats(attack=2 if self.golden else 1, temp=True, reason=StatChangeCause.AURA_BUFF,
                                          source=self, *args, **kwargs)
