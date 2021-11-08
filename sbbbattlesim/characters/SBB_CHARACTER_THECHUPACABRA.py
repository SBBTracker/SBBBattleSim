from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import get_behind_targets, StatChangeCause


class CharacterType(Character):
    display_name = 'The Chupacabra'
    slay = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.ChupacabraSlay)

    class ChupacabraSlay(OnAttackAndKill):
        slay = True
        def handle(self, killed_character, *args, **kwargs):
            behind_targets = get_behind_targets(self.manager.position)
            targetted_chars = [c for c in self.manager.owner.valid_characters() if c.position in behind_targets]

            modifier = 2 if self.manager.golden else 2
            for char in [self.manager, *targetted_chars]:
                char.change_stats(attack=modifier, health=modifier, temp=False,
                                  reason=StatChangeCause.SLAY, source=self.manager)

