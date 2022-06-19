from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill
from sbbbattlesim.utils import Tribe


class BravePrincessSlay(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, *args, **kwargs):
        if self.manager not in self.manager.player.combat_records:
            self.manager.quest_counter -= 1
            if self.manager.quest_counter <= 0 :
                self.manager.player.completed_quests.append(self.source)
                # self.manager.unregister(self)


class CharacterType(Character):
    display_name = 'Brave Princess'
    quest = True

    _attack = 5
    _health = 3
    _level = 3
    _tribes = {Tribe.GOOD, Tribe.ROYAL}
    _quest_counter = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.golden:
            self.register(BravePrincessSlay)
