from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
import random
from sbbbattlesim.utils import StatChangeCause, Tribe


class TreasureType(Treasure):
    display_name = 'Ancient Sarcophagus'
    aura = True

    def buff(self, target_character):
        if Tribe.EVIL in target_character.tribes:

            class AncientSarcophagusOnDeath(OnDeath):
                ancient_sarcophagus = self
                last_breath = False

                def handle(self, *args, **kwargs):
                    for _ in range(self.ancient_sarcophagus.mimic + 1):
                        valid_targets = self.manager.owner.opponent.valid_characters()
                        if valid_targets:
                            target = random.choice(valid_targets)
                            target.change_stats(damage=3, reason=StatChangeCause.ANCIENT_SARCOPHAGUS, source=self.ancient_sarcophagus)

            target_character.register(AncientSarcophagusOnDeath, temp=True)
