from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Fanny'
    support = True

    _attack = 2
    _health = 2
    _level = 2
    _tribes = {Tribe.DWARF, }

    def buff(self, target_character, *args, **kwargs):
        if Tribe.DWARF in target_character.tribes:
            stat_change = 4 if self.golden else 2
            with Buff(reason=StatChangeCause.SUPPORT_BUFF, source=self, targets=[target_character],
                      attack=stat_change, health=stat_change, temp=True, *args, **kwargs):
                pass
