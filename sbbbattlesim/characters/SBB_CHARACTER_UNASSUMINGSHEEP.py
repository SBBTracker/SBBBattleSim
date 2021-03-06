import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class SheepWolfLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        stat = 12 if self.manager.golden else 6
        sheep = [
            character_registry['SBB_CHARACTER_EVILWOLF'](
                self.manager.player, self.manager.position, stat, stat,
                golden=False, keywords=[], tribes=['evil', 'animal'], cost=1
            )
        ]
        self.manager.player.summon(self.manager.position, sheep)


class CharacterType(Character):
    display_name = '''Sheep in Wolfs Clothing'''
    last_breath = True

    _attack = 2
    _health = 2
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(SheepWolfLastBreath)
