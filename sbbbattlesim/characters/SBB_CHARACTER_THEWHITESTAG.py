from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnPreAttack
from sbbbattlesim.utils import get_behind_targets, Tribe


class TheWhiteStagOnPreAttack(OnPreAttack):
    def handle(self, *args, **kwargs):
        behind_targets = get_behind_targets(self.manager.position)
        targetted_chars = [c for c in self.manager.player.valid_characters() if c.position in behind_targets]
        modifier = 6 if self.manager.golden else 3

        Buff(reason=ActionReason.THE_WHITE_STAG_BUFF, source=self.source, targets=targetted_chars,
             attack=modifier, health=modifier, temp=False).resolve()


class CharacterType(Character):
    display_name = 'The White Stag'

    _attack = 3
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ANIMAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.register(TheWhiteStagOnPreAttack)
