import logging
import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class TrojanDonkeySummon(OnDamagedAndSurvived):
    def handle(self, *args, **kwargs):
        if self.manager.golden:
            _lambda = lambda char: char._level == self.manager.player.level and char.id != "SBB_CHARACTER_TROJANDONKEY"
        else:
            _lambda = lambda char: char._level <= self.manager.player.level

        valid_summons = [*character_registry.filter(_lambda=_lambda)]
        if valid_summons:
            _summon = random.choice(valid_summons)
            summon = _summon.new(
                player=self.manager.player,
                position=self.manager.position,
                golden=False
            )
            self.manager.player.summon(self.manager.position, [summon])


class CharacterType(Character):
    display_name = 'Trojan Donkey'

    _attack = 2
    _health = 6
    _level = 3
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register(TrojanDonkeySummon)
