import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)


class BeardedVultureOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        stat_change = 6 if self.bearded_vulture.golden else 3
        Buff(source=self.bearded_vulture, reason=StatChangeCause.BEARDEDVULTURE_BUFF, targets=[self.bearded_vulture],
             attack=stat_change, health=stat_change, temp=False).resolve()


class CharacterType(Character):
    display_name = 'Bearded Vulture'
    aura = True

    _attack = 3
    _health = 3
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def buff(self, target_character, *args, **kwargs):
        # Give animals minions the buff
        if Tribe.ANIMAL in target_character.tribes and target_character is not self:
            target_character.register(BeardedVultureOnDeath, temp=True, bearded_vulture=self)
