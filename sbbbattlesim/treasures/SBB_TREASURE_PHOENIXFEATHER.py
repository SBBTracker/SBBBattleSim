from sbbbattlesim.action import Aura
from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure
import copy

class PhoenixFeatherOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        if not self.feather.feather_used and self.manager in self.manager.player.graveyard:

            all_characters = self.manager.player.valid_characters() + [self.manager]
            max_attack = max(all_characters, key=lambda x: x.attack).attack
            if self.manager.attack >= max_attack:
                self.manager._damage = 0
                self.manager.dead = False
                self.manager.player.graveyard.remove(self.manager)
                self.manager.player.summon(self.manager.position, [self.manager])

                if self.feather.mimic:
                    new_char = self.manager.__class__(
                        self.manager.player,
                        self.manager.position,
                        self.manager._base_attack,
                        self.manager._base_health,
                        golden=self.manager.golden,
                        tribes=self.manager.tribes,
                        cost=self.manager.cost
                    )
                    new_char._action_history = copy.copy(self.manager._action_history)  #TODO this need to be part of a new copy function

                    self.manager.player.summon(self.manager.position, [new_char], *args, **kwargs)

                self.feather.feather_used = True


class TreasureType(Treasure):
    display_name = 'Phoenix Feather'
    aura = True

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False
        self.aura = Aura(event=PhoenixFeatherOnDeath, source=self, priority=1000, feather=self)

    
