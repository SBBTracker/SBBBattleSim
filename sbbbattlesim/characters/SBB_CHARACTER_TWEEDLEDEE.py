import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath


class CharacterType(Character):
    display_name = 'Tweedle Dee'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(self.TweedleDeeLastBreath)

    class TweedleDeeLastBreath(OnDeath):
        last_breath = True
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.priority = sbbbattlesim.SUMMONING_PRIORITY

        def handle(self, *args, **kwargs):
            attack, health = (2,8) if self.manager.golden else (1,4)
            tweedle_dum = [character_registry['Tweedle Dum'](self.manager.owner, self.manager.position, attack, health, golden=False, keywords=[], tribes=['dwarf'], cost=1)]
            self.manager.owner.summon(self.manager.position, *tweedle_dum)
