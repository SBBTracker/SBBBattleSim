from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttack
from sbbbattlesim.utils import get_behind_targets


class CharacterType(Character):
    display_name = 'Copycat'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.CopycatOnAttack)

    class CopycatOnAttack(OnAttack):
        def handle(self, *args, **kwargs):
            behind_targets = get_behind_targets(self.manager.position)
            targetted_chars = [c for c in self.manager.owner.valid_characters() if c.position in behind_targets]

            itr = 2 if self.golden else 1
            for char in targetted_chars:
                for _ in itr:
                    char('OnLastBreath', *args, **kwargs)





