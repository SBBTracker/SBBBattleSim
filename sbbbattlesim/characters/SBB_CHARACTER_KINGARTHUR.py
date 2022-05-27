from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import Tribe


class PrinceArthurOnStart(OnStart):
    def handle(self, stack, *args, **kwargs):
        stat_change = 4 if self.source.golden else 2
        royals = self.source.player.valid_characters(
            _lambda=lambda char: char.golden and (Tribe.PRINCE in char.tribes or Tribe.PRINCESS in char.tribes)
        )
        Buff(source=self.source, reason=ActionReason.PRINCEARTHUR_BUFF, targets=royals,
             attack=stat_change, health=stat_change, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Prince Arthur'

    _attack = 5
    _health = 5
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.PRINCE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player.register(PrinceArthurOnStart, priority=80, source=self)
