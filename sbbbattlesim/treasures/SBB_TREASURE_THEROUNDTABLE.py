from sbbbattlesim.treasures import Treasure
from sbbbattlesim.utils import StatChangeCause
from sbbbattlesim.events import OnStart


class TreasureType(Treasure):
    display_name = 'The Round Table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class RoundTableBuff(OnStart):
            table = self

            def handle(self, *args, **kwargs):
                for _ in range(bool(self.table.mimic) + 1):
                    for char in self.manager.valid_characters():
                        if char.attack > char.health:
                            char.change_stats(health=char.attack - char.health, reason=StatChangeCause.ROUND_TABLE_BUFF,
                                              source=self.table, temp=False)
                        else:
                            char.change_stats(attack=char.health - char.attack, reason=StatChangeCause.ROUND_TABLE_BUFF,
                                              source=self.table, temp=False)

        self.player.register(RoundTableBuff)
