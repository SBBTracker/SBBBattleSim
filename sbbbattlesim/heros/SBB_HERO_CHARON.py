from sbbbattlesim.events import OnDeath
from sbbbattlesim.heros import Hero
from sbbbattlesim.utils import StatChangeCause

CHARON_STR = 'SBB_HER_CHARON'

class HeroType(Hero):
    display_name = 'Charon'
    aura = True

    def buff(self, target_character):
        class CharonOnDeath(OnDeath):
            priority = 999
            last_breath = False
            charon = self

            def handle(self, *args, **kwargs):
                # This should only proc once per combat
                if self.manager.owner.stateful_effects.get(CHARON_STR, False):
                    return  # This has already procced
                self.manager.owner.stateful_effects[CHARON_STR] = True

                self.manager.change_stats(attack=2, health=1, reason=StatChangeCause.CHARON_BUFF, source=self.charon)

        target_character.register(CharonOnDeath)

