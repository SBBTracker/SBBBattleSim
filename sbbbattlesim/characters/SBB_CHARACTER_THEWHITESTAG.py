from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttack
from sbbbattlesim.utils import get_behind_targets


class CharacterType(Character):
    display_name = 'The White Stag'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.TheWhiteStagOnAttack)

    class TheWhiteStagOnAttack(OnAttack):
        def handle(self, *args, **kwargs):
            behind_targets = get_behind_targets(self.manager.position)
            targetted_chars = [c for c in self.manager.owner.valid_characters() if c.position in behind_targets]

            modifier = 6 if self.manager.golden else 3
            for char in targetted_chars:
                char.change_stats(attack=modifier, health=modifier, temp=False,
                                  reason=f'{self} buff on targets behind me')





