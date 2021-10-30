from sbbbattlesim.characters import Character
from sbbbattlesim.events import Death


class CharacterType(Character):
    # PUFF PUFF VARIABLE
    # Store the global Puff Puff buff
    display_name = 'PUFF PUFF'

    class PuffPuffDeath(Death):
        def __call__(self, **kwargs):
            setattr(self.manager.owner, 'puffpuffbuff', getattr(self.manager.owner, 'puffpuffbuff', 0) + 2 if self.golden else 1)

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
