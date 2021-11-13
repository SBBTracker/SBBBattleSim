import random

from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Wretched Mummy'
    last_breath = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.WretchedMummyDeath)

    class WretchedMummyDeath(OnDeath):
        last_breath = True
        def handle(self, *args, **kwargs):
            valid_targets = self.manager.owner.opponent.valid_characters()
            if valid_targets:
                target = random.choice(valid_targets)
                target.change_stats(damage=self.manager.attack, reason=StatChangeCause.WRETCHED_MUMMY_EXPLOSION, source=self.manager)
    #todo add golden effect