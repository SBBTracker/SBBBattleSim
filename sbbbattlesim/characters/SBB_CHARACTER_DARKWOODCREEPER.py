from sbbbattlesim.action import Buff, EventAura
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe, StatChangeCause


class DarkwoodCreeperOnDamage(OnDamagedAndSurvived):
    def handle(self, stack, *args, **kwargs):
        Buff(
            reason=StatChangeCause.DARKWOOD_CREEPER_BUFF,
            source=self.darkwood,
            targets=[self.manager],
            attack=2 if self.darkwood.golden else 1,
            temp=False,
            stack=stack
        ).resolve()


class CharacterType(Character):
    display_name = 'Darkwood Creeper'
    aura = True

    _attack = 0
    _health = 3
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = EventAura(reason=StatChangeCause.AURA_BUFF, source=self, darkwood=self, event=DarkwoodCreeperOnDamage)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
