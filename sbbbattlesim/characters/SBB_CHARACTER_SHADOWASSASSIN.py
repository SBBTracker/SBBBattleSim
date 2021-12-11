from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import StatChangeCause, Tribe


class ShadowAssassinOnSlay(OnSlay):
    def handle(self, source, stack, *args, **kwargs):
        attack_buff, health_buff = (2, 2) if self.shadow_assassin.golden else (1, 1)

        with Buff(reason=StatChangeCause.SHADOW_ASSASSIN_ON_SLAY_BUFF, source=self.shadow_assassin, targets=[self.shadow_assassin],
                  attack=attack_buff, health=health_buff, temp=False, stack=stack, *args, **kwargs):
            pass


class CharacterType(Character):
    display_name = 'Shadow Assassin'
    aura = True

    _attack = 2
    _health = 1
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def buff(self, target_character, *args, **kwargs):
        target_character.register(ShadowAssassinOnSlay, temp=True, shadow_assassin=self)
