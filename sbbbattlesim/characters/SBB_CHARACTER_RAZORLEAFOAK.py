import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath, OnDamagedAndSurvived
import sbbbattlesim
from sbbbattlesim.utils import Tribe, StatChangeCause


class CharacterType(Character):
    display_name = 'Broc Lee'

    _attack = 0
    _health = 15
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class BrocLeeOnDamageAndSurvived(OnDamagedAndSurvived):
            def handle(self, *args, **kwargs):
                self.manager.change_stats(attack=20 if self.manager.golden else 10, reason=StatChangeCause.BROC_LEE_BUFF, source=self.manager)

        self.register(BrocLeeOnDamageAndSurvived)
