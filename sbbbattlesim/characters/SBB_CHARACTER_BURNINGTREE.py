from sbbbattlesim.action import ActionReason, Buff

from sbbbattlesim.events import OnBuff

from sbbbattlesim.characters import Character

from sbbbattlesim.utils import Tribe


class BurningTreeOnBuff(OnBuff):
    def handle(self, reason, stack, attack, health, *args, **kwargs):
        if reason in [ActionReason.BURNING_TREE_BUFF]:
            return
        golden_multiplier = 2 if self.source.golden else 1
        Buff(reason=ActionReason.BURNING_TREE_BUFF, source=self.source, targets=[self.source],
             health=attack * golden_multiplier, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Burning Tree'

    _attack = 4
    _health = 20
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register(BurningTreeOnBuff, priority=9999)
