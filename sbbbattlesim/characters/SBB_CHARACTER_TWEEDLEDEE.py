import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe
from sbbbattlesim.action import Buff, ActionReason


class TweedleDeeLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        attack, health = (self.manager.max_health * 2, self.manager.attack * 2) if self.manager.golden else (
        self.manager.max_health, self.manager.attack)
        tweedle_dum = [
            character_registry['Tweedle Dum'](
                self.manager.player, self.manager.position, 0, 1,
                golden=False, keywords=[], tribes=['dwarf'], cost=1
            )
        ]

        self.manager.player.summon(self.manager.position, tweedle_dum)
        Buff(reason=ActionReason.TWEEDLEDEE_BUFF, source=self.manager, targets=tweedle_dum,
             attack=attack, health=health,
             temp=False, stack=stack).execute().resolve()
        Buff(reason=ActionReason.TWEEDLEDEE_BUFF, source=self.manager, targets=tweedle_dum,
             health=-1,
             temp=False, stack=stack).execute().resolve()


class CharacterType(Character):
    display_name = 'Tweedle Dee'
    last_breath = True

    _attack = 3
    _health = 2
    _level = 3
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(TweedleDeeLastBreath)
