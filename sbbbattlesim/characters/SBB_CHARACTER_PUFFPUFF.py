from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath


class CharacterType(Character):
    # PUFF PUFF VARIABLE
    # Store the global Puff Puff buff
    # THIS IS WRONG
    display_name = 'PUFF PUFF'

    class PuffPuffDeath(OnDeath):
        def handle(self, *args, **kwargs):
            stat_change = 2 if self.managergolden else 1
            setattr(self.manager.owner, 'puffpuffbuff', getattr(self.manager.owner, 'puffpuffbuff', 0) + stat_change)
            # TODO Trigger On Buff

    def __init__(self, attack, health, golden=False, keywords=[], tribes=[]):
        super().__init__(
            attack=attack,
            health=health,
            golden=golden,
            keywords=keywords,
            tribes=tribes
        )

        ppb = getattr(self.owner, 'puffpuffbuff', None)
        new_ppb = min(attack, health) - (12 if golden else 6)
        puffpuffbuff = min(ppb, new_ppb) if ppb is not None else new_ppb
        setattr(self.owner, 'puffpuffbuff', puffpuffbuff)

        self.register(self.PuffPuffDeath)

    @property
    def attack(self):
        return self.base_attack + self.attack_bonus + getattr(self.owner, 'puffpuffbuff', 0)

    @property
    def health(self):
        return self.base_health + self.health_bonus - self.damage + getattr(self.owner, 'puffpuffbuff', 0)
