from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe, StatChangeCause


class DarkwoodCreeperOnDamage(OnDamagedAndSurvived):
    def handle(self, stack, *args, **kwargs):
        self.manager.change_stats(
            attack=2 if self.darkwood.golden else 1,
            temp=False,
            reason=StatChangeCause.DARKWOOD_CREEPER_BUFF,
            source=self.darkwood,
            stack=stack
        )


class CharacterType(Character):
    display_name = 'Darkwood Creeper'
    aura = True

    _attack = 0
    _health = 3
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def buff(self, target_character, *args, **kwargs):
        target_character.register(DarkwoodCreeperOnDamage, temp=True, darkwood=self)
