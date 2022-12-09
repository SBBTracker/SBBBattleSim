from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import get_behind_targets, Tribe


class ChupacabraSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        modifier = 2 if self.manager.golden else 1

        Buff(reason=ActionReason.CHUPACABRA_SLAY, source=self.manager,
             targets=self.manager.player.valid_characters(_lambda=lambda char: Tribe.MONSTER in char.tribes),
             attack=modifier, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'The Chupacabra'

    _attack = 8
    _health = 6
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(ChupacabraSlay)
