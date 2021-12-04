import logging
import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath, OnDamagedAndSurvived
import sbbbattlesim
from sbbbattlesim.utils import Tribe


logger = logging.getLogger(__name__)


class CharacterType(Character):
    display_name = 'Trojan Donkey'

    _attack = 1
    _health = 5
    _level = 3
    _tribes = {Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register(self.TrojanDonkeySummon)

    class TrojanDonkeySummon(OnDamagedAndSurvived):

        def handle(self, *args, **kwargs):
            if self.manager.golden:
                _lambda = lambda char: char._level == self.manager.owner.level
            else:
                _lambda = lambda char: char._level <= self.manager.owner.level

            valid_summons = [*character_registry.filter(_lambda=_lambda)]
            if valid_summons:
                _summon = random.choice(valid_summons)
                summon = _summon.new(
                    owner=self.manager.owner,
                    position=self.manager.position,
                    golden=False
                )
                self.manager.owner.summon(self.manager.position, [summon])