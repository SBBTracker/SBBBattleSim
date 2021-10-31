from sbbbattlesim import utils
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnStart


class CharacterType(Character):
    display_name = 'Heartwood Elder'

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
                             char.change_stats(attack=stat_change, health=stat_change, temp=False, reason=f'{self.heartwood} OnStart Support Buff')

        self.owner.register(HeartWoodOnStart)
