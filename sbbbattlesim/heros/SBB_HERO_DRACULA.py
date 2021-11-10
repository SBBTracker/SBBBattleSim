from sbbbattlesim.events import OnDeath, OnAttackAndKill
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import Tribe, StatChangeCause


class HeroType(Hero):
    display_name = 'Sad Dracula'
    aura = True

    def buff(self, target_character):
        if target_character.position == 1:
            class SadDraculaOnAttackAndKill(OnAttackAndKill):
                sad_dracula = self

                def handle(self, killed_character, *args, **kwargs):
                    self.manager.change_stats(attack=3, reason=StatChangeCause.SAD_DRACULA_SLAY, source=self.sad_dracula)

            target_character.register(SadDraculaOnAttackAndKill)
