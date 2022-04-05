import sbbbattlesim
from sbbbattlesim.characters import Character
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe
from sbbbattlesim.action import Buff, ActionReason


class TweedleDeeLastBreath(OnDeath):
    last_breath = True

    def handle(self, stack, reason, *args, **kwargs):
        attack, health = (self.manager.max_health * 2, self.manager.attack * 2) if self.manager.golden else (self.manager.max_health, self.manager.attack)
        tweedle_dum = character_registry['SBB_CHARACTER_TWEEDLEDUM'].new(self.manager.player, self.manager.position, golden=False)
        self.manager.player.summon(self.manager.position, [tweedle_dum])

        Buff(reason=ActionReason.TWEEDLEDEE_BUFF, source=self.manager, attack=attack, health=health, stack=stack).execute(tweedle_dum)


class CharacterType(Character):
    display_name = 'Tweedle Dee'
    last_breath = True

    _attack = 10
    _health = 3
    _level = 5
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(TweedleDeeLastBreath)
