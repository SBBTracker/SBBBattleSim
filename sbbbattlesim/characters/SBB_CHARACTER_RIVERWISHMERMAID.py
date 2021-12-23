from sbbbattlesim.action import Buff, Support, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class RiverwishMermaidOnAttackAndKill(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        stats = 2 if self.source.golden else 1
        Buff(reason=ActionReason.SUPPORT_BUFF, source=self.source, targets=[self.manager], attack=stats, health=stats,
             stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Riverwish Mermaid'
    support = True

    _attack = 4
    _health = 8
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PRINCESS}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support = Support(source=self, event=RiverwishMermaidOnAttackAndKill)
