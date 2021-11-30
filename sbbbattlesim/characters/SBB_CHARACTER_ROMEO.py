from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath, OnSummon
import sbbbattlesim
from sbbbattlesim.characters import registry as character_registry

import random

from sbbbattlesim.utils import Tribe, StatChangeCause

JULIET_ID = 'SBB_CHARACTER_JULIET'

class CharacterType(Character):
    display_name = 'Romeo'
    last_breath = True

    _attack = 5
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.PRINCE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.RomeoLastBreath.romeo = self

        self.register(self.RomeoLastBreath)

    class RomeoLastBreath(OnDeath):
        last_breath = True

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            dead_juliets = [j for j in self.manager.owner.graveyard if j.id == JULIET_ID]
            if dead_juliets:

                juliet = max(dead_juliets, key=lambda juliet : (juliet.attack, juliet.health))
                juliet._damage = 0  # Reset damage dealt to this unit

                class RomeoOnSummon(OnSummon):
                    romeo = self.romeo

                    def handle(self, summoned_characters, stack, *args, **kwargs):
                        modifier = 14 if self.romeo.golden else 7
                        self.juliet.change_stats(
                            reason=StatChangeCause.ROMEO_BUFF, attack=modifier,
                            health=modifier, temp=False, source=self.romeo
                        )

                RomeoOnSummon.juliet = juliet

                juliet.owner.register(RomeoOnSummon)
                self.manager.owner.summon(self.manager.position, [juliet])

