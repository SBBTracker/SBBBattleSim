from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Darkwood Creeper'

    _attack = 0
    _health = 3
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def buff(self, target_character):

        class DarkwoodCreeperOnDamage(OnDamagedAndSurvived):
            def __call__(self, **kwargs):
                attack_buff = 2 if self.character.golden else 1
                self.character.attack += attack_buff
                return 'OnBuff', {'attack_buff': attack_buff}

        target_character.register(DarkwoodCreeperOnDamage, temp=True)
