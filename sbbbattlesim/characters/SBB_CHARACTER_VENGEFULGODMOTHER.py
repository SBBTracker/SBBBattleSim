from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe


class NutCrackerOnDamageAndSurvive(OnDamagedAndSurvived):
    def handle(self, stack, reason, *args, **kwargs):
        if self.manager not in self.manager.player.combat_records:
            self.manager.quest_counter -= 1
            if self.manager.quest_counter <= 0:
                self.manager.player.completed_quests.append(self.source)
                self.manager.unregister(self)


class CharacterType(Character):
    display_name = 'Nutcracker'
    quest = True

    _attack = 4
    _health = 10
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.TREANT}
    _quest_counter = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.golden:
            self.register(NutCrackerOnDamageAndSurvive)

