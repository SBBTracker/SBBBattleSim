from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnDeath
import random
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Ancient Sarcophagus'
    aura = True

    def buff(self, target_character):
        if 'evil' in target_character.tribes:
            class AncientSarcophagusOnDeath(OnDeath):
                ancient_sarcophagus = self

                def handle(self, *args, **kwargs):
                    itr = 1  # TODO this may be useful when dealing with mimic

                    for _ in range(itr):
                        valid_targets = self.manager.owner.opponent.valid_characters()

                        if valid_targets:
                            target = random.choice(valid_targets)
                            target.changestats(damage=3, reason=StatChangeCause.ANCIENT_SARCOPHAGUS,
                                               source=self.ancient_sarcophagus)

            target_character.register(AncientSarcophagusOnDeath, temp=True)
