import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe


class CharacterType(Character):
    display_name = 'Tweedle Dee'
    last_breath = True

    _attack = 3
    _health = 2
    _level = 3
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.TweedleDeeLastBreath)

    class TweedleDeeLastBreath(OnDeath):
        last_breath = True
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            attack, health = (4, 6) if self.manager.golden else (2, 3)
            tweedle_dum = [
                character_registry['Tweedle Dum'](
                    self.manager.owner, self.manager.position, attack, health,
                    golden=False, keywords=[], tribes=['dwarf'], cost=1
                )
            ]
            self.manager.owner.summon(self.manager.position, tweedle_dum)
