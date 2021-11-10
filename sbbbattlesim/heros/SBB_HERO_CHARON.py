import random

from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero


CHARON_STR = 'SBB_HER_CHARON'

class HeroType(Hero):
    display_name = 'Charon'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class CharonOnDeath(OnDeath):
            priority = 999

            def handle(self, *args, **kwargs):
                itr = 1  # TODO this may be useful when dealing with mimic
                # TODO update this treasure

                # This should only proc once per combat
                if self.manager.owner.stateful_effects.get(CHARON_STR, False):
                    return  # This has already procced
                self.manager.owner.stateful_effects[CHARON_STR] = True

                for _ in range(itr):
                    self.manager._base_health += 2
                    self.manager._base_attack += 1

        self.player.register(CharonOnDeath)