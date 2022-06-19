from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill, OnBuff, OnStart
from sbbbattlesim.utils import Tribe


class LancelotSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        modifier = 4 if self.manager.golden else 2
        Buff(reason=ActionReason.LANCELOT_SLAY, source=self.manager, attack=modifier, health=modifier).execute(self.manager)


class LancelotOnBuff(OnBuff):
    def handle(self, stack, attack, health, reason=None, *args, **kwargs):
        self.source.progress_quest(1)


class LancelotOnStart(OnStart):
    def handle(self, stack, reason=None, *args, **kwargs):
        self.source.progress_quest(1)


class CharacterType(Character):
    display_name = 'Lancelot'
    quest = True

    _attack = 9
    _health = 9
    _level = 5
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
    _quest_counter = 25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(LancelotSlay)

        self.lance_on_start_event = None
        self.lance_on_buff_event = None
        if not self.golden:
            self.lance_on_start_event = self.player.register(LancelotOnStart, source=self)
            self.lance_on_buff_event = self.register(LancelotOnBuff, source=self)

    def progress_quest(self, amount):
        if max(self.attack, self.health) >= 25:
            super().progress_quest(1)
            self.player.unregister(self.lance_on_start_event)
            self.unregister(self.lance_on_buff_event)