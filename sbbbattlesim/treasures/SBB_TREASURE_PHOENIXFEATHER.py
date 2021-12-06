from sbbbattlesim.events import OnDeath
from sbbbattlesim.treasures import Treasure


class PhoenixFeatherOnDeath(OnDeath):
    last_breath = False

    def handle(self, *args, **kwargs):
        if not self.feather.feather_used and self.manager in self.manager.owner.graveyard:

            all_characters = self.manager.owner.valid_characters() + [self.manager]
            max_attack = max(all_characters, key=lambda x: x.attack).attack
            if self.manager.attack >= max_attack:
                self.manager._damage = 0
                self.manager.dead = False
                self.manager.owner.graveyard.remove(self.manager)
                self.manager.owner.summon(self.manager.position, [self.manager])

                if self.feather.mimic:
                    new_char = self.manager.__class__(
                        self.manager.owner,
                        self.manager.position,
                        self.manager.attack,
                        self.manager.health,
                        golden=self.manager.golden,
                        tribes=self.manager.tribes,
                        cost=self.manager.cost
                    )

                    self.manager.owner.summon(self.manager.position, [new_char])

                self.feather.feather_used = True


class TreasureType(Treasure):
    display_name = 'Phoenix Feather'
    aura = True

    _level = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feather_used = False

    def buff(self, target_character, *args, **kwargs):
        target_character.register(PhoenixFeatherOnDeath, temp=True, priority=1000, feather=self)
