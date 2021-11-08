from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause


class CharacterType(Character):
    display_name = 'Heartwood Elder'
    support = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class HeartWoodOnStart(OnStart):
            heartwood = self
            def handle(self, *args, **kwargs):
                stat_change = 4 if self.heartwood.golden else 2
                for pos in utils.get_support_targets(self.heartwood.position, horn='SBB_TREASURE_BANNEROFCOMMAND' in self.manager.treasures):
                    char = self.manager.characters[pos]
                    if char is not None:
                         if 'treant' in char.tribes:
                             char.change_stats(attack=stat_change, health=stat_change, temp=False,
                                               reason=StatChangeCause.HEARTWOOD_BUFF, source=self)

        self.owner.register(HeartWoodOnStart)

    def buff(self, target_character):
        pass
