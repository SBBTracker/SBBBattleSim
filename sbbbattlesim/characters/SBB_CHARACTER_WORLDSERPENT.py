from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Jormungandr'
    slay = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.JormungandrOnAttackAndKill)

    class JormungandrOnAttackAndKill(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            modifier = 40 if self.manager.golden else 20
            self.manager.change_stats(attack=modifier, health=modifier, temp=False, reason=StatChangeCause.SLAY, source=self.manager)