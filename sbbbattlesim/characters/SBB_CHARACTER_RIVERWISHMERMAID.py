from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Riverwish Mermaid'
    support = True

    def buff(self, target_character):

        class RiverwishMermaidBuff(OnAttackAndKill):
            slay = True
            riverwish_mermaid = self

            def handle(self, killed_character, *args, **kwargs):
                stats = 2 if self.riverwish_mermaid.golden else 1
                self.manager.change_stats(attack=stats, health=stats, temp=False, reason=StatChangeCause.SUPPORT_BUFF, source=self)

        target_character.register(RiverwishMermaidBuff, temp=True)


