from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import get_behind_targets, Tribe


class ChupacabraSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        behind_targets = get_behind_targets(self.manager.position)
        targetted_chars = [c for c in self.manager.player.valid_characters() if c.position in behind_targets]

        modifier = 4 if self.manager.golden else 2

        Buff(reason=ActionReason.CHUPACABRA_SLAY, source=self.manager, targets=[self.manager, *targetted_chars],
             attack=modifier, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'The Chupacabra'

    _attack = 7
    _health = 5
    _level = 4
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(ChupacabraSlay)
