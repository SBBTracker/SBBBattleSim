from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import get_behind_targets, Tribe


class CharacterType(Character):
    display_name = 'Copycat'

    _attack = 2
    _health = 12
    _level = 4
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.CopycatOnPreAttack)

    class CopycatOnPreAttack(OnPreAttack):
        def handle(self, *args, **kwargs):
            behind_targets = get_behind_targets(self.manager.position)
            targetted_chars = [c for c in self.manager.owner.valid_characters() if c.position in behind_targets]

            itr = 2 if self.manager.golden else 1
            for _ in range(itr):
                for char in targetted_chars:
                    char('OnDeath', *args, **kwargs)
                    #TODO instead of calling ondeath create an ephemeral event manager to handle both events with a custom stack

