from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe, random_combat_spell


class CharacterType(Character):
    display_name = 'Monster Book'
    last_breath = True

    _attack = 10
    _health = 5
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class MonsterBookOnDeath(OnDeath):
            last_breath = True

            def handle(self, *args, **kwargs):
                random_combat_spell(self.owner.level).cast()

        self.register(MonsterBookOnDeath)
