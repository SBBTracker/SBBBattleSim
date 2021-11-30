from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause


class HeroType(Hero):
    display_name = 'Sad Dracula'
    aura = True

    def buff(self, target_character, *args, **kwargs):
        if target_character.position == 1:
            class SadDraculaOnAttackAndKill(OnAttackAndKill):
                sad_dracula = self
                slay = True

                def handle(self, killed_character, stack, *args, **kwargs):
                    self.manager.change_stats(attack=3, reason=StatChangeCause.SAD_DRACULA_SLAY, source=self.sad_dracula, stack=stack)

            target_character.register(SadDraculaOnAttackAndKill, temp=True)
