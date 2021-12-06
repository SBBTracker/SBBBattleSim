from sbbbattlesim.characters import Character
from sbbbattlesim.utils import Tribe, StatChangeCause


class CharacterType(Character):
    display_name = 'Rainbow Unicorn'
    aura = True

    _attack = 1
    _health = 5
    _level = 2
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def buff(self, target_character, *args, **kwargs):
        if Tribe.GOOD in target_character.tribes and target_character != self:
            target_character.change_stats(health=2 if self.golden else 1, temp=True, source=self,
                                          reason=StatChangeCause.RAINBOWUNICORN_BUFF, *args, **kwargs)
