from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import get_behind_targets, Tribe


class CharacterType(Character):
    display_name = 'The White Stag'

    _attack = 3
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.TheWhiteStagOnPreAttack)

    class TheWhiteStagOnPreAttack(OnPreAttack):
        def handle(self, *args, **kwargs):
            behind_targets = get_behind_targets(self.manager.position)
            targetted_chars = [c for c in self.manager.owner.valid_characters() if c.position in behind_targets]

            modifier = 6 if self.manager.golden else 3
            for char in targetted_chars:
                char.change_stats(attack=modifier, health=modifier, temp=False,
                                  reason=f'{self} buff on targets behind me')





