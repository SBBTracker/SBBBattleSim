from sbbbattlesim.action import Aura, Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import Tribe


class ShadowAssassinOnSlay(OnSlay):
    def handle(self, source, stack, *args, **kwargs):
        attack_buff = 2 if self.source.golden else 1
        Buff(reason=ActionReason.SHADOW_ASSASSIN_ON_SLAY_BUFF, source=self.source, targets=[self.source],
             attack=attack_buff, stack=stack, *args, **kwargs).resolve()


class CharacterType(Character):
    display_name = 'Shadow Assassin'
    ranged = True
    aura = True

    _attack = 2
    _health = 4
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, event=ShadowAssassinOnSlay)
