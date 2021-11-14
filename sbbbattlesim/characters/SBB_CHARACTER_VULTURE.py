from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
import logging

from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Bearded Vulture'
    aura = True

    _attack = 3
    _health = 3
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def buff(self, target_character):
        class BeardedVultureOnDeath(OnDeath):
            bearded_vulture = self
            def handle(self, *args, **kwargs):
                stat_change = 6 if self.bearded_vulture.golden else 3
                self.bearded_vulture.change_stats(attack=stat_change, health=stat_change, temp=False,
                                                  reason=f'{self.manager} died and Bearded Vulture triggered')

        # Give animals minions the buff
        if 'animal' in target_character.tribes and target_character is not self:
            target_character.register(BeardedVultureOnDeath, temp=True)