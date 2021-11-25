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
    last_breath = True

    _attack = 15
    _health = 15
    _level = 6
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class TrojanDonkeySummon(OnDamagedAndSurvived):
            def handle(self, *args, **kwargs):
                valid_summons = [*character_registry.filter(_lambda=lambda char: char._level == self.manager.owner.level)]
                if valid_summons:
                    summon = random.choice(valid_summons).new(
                        owner=self.manager.owner,
                        position=self.manager.position,
                        golden=self.manager.golden
                    )
                    self.manager.owner.summon(self.manager.position, summon)

        self.register(TrojanDonkeySummon)
