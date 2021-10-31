from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSummon
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Hungry Hungry Hippocampus'

    def buff_player(self, player):
        class HungryHungryHippocampusOnSummon(OnSummon):
            hungry_hungry_hippocampus = self

            def handle(self, summoned_characters, *args, **kwargs):
                num_animals = len(list(filter(lambda char: 'animal' in char.tribes, summoned_characters)))
                modifier = 4 if self.hungry_hungry_hippocampus.golden else 2

                if self.hungry_hungry_hippocampus in self.manager.characters.values():
                    self.hungry_hungry_hippocampus.change_stats(health=num_animals*modifier, temp=False,
                                                                reason=f'{self.manager} gets health from summoned animals')

        player.register(HungryHungryHippocampusOnSummon, temp=True)
