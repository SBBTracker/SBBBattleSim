from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Lancelot'
    slay = True
    quest = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class LancelotSlay(OnAttackAndKill):
            slay = True

            def handle(self, killed_character, *args, **kwargs):
                modifier = 4 if self.manager.golden else 2
                self.manager.change_stats(attack=modifier, health=modifier, temp=False, reason=StatChangeCause.SLAY,
                                          source=self.manager)

        self.register(LancelotSlay)

