from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived


class DarkwoodCreeperOnDamage(OnDamagedAndSurvived):
    def __call__(self, **kwargs):
        attack_buff = 2 if self.character.golden else 1
        self.character.attack += attack_buff
        return 'OnBuff', {'attack_buff': attack_buff}


class CharacterType(Character):
    name = 'Darkwood Creeper'

    def buff(self, target_character):
        target_character.register(DarkwoodCreeperOnDamage, temp=True)
