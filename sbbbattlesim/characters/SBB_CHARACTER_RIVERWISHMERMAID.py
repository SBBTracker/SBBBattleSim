from sbbbattlesim.action import Buff, SupportBuff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import StatChangeCause, Tribe


class RiverwishMermaidOnAttackAndKill(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        stats = 2 if self.riverwish_mermaid.golden else 1
        Buff(reason=StatChangeCause.SUPPORT_BUFF, source=self.riverwish_mermaid, targets=[self.manager],
             attack=stats, health=stats, temp=False, stack=stack).resolve()


class RiverwishMermaidSupportBuff(SupportBuff):
    def execute(self, character, *args, **kwargs):
        character.register(RiverwishMermaidOnAttackAndKill, riverwish_mermaid=self.source, temp=True, *args, **kwargs)


class CharacterType(Character):
    display_name = 'Riverwish Mermaid'
    support = True

    _attack = 4
    _health = 4
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PRINCESS}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support_buff = RiverwishMermaidSupportBuff(source=self)

    def buff(self, target_character, *args, **kwargs):
        self.support_buff.execute(target_character, *args, **kwargs)
