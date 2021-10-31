from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill


class CharacterType(Character):
    display_name = 'Riverwish Mermaid'
    support = True

    def buff(self, target_character):

        class RiverwishMermaidBuff(OnAttackAndKill):
            riverwish_mermaid = self

            def handle(self, *args, **kwargs):
                stats = 2 if self.riverwish_mermaid.golden else 1
                self.manager.change_stats(attack=stats, health=stats, temp=False,
                                          reason='{self.riverwish_mermaid} gave {self} slay from which I am gaining stats')

        target_character.register(RiverwishMermaidBuff, temp=True)


