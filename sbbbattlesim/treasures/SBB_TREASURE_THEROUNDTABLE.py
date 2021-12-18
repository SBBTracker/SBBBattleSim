from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.events import OnStart
from sbbbattlesim.treasures import Treasure


class TreasureType(Treasure):
    display_name = 'The Round Table'

    _level = 7

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class RoundTableBuff(OnStart):
            priority = 30
            table = self

            def handle(self, stack, *args, **kwargs):
                for _ in range(bool(self.table.mimic) + 1):
                    change_dt = {}
                    for char in self.table.player.valid_characters():
                        if char.attack > char.health:
                            change_dt[char] = (0, char.attack - char.health)
                        else:
                            change_dt[char] = (char.health - char.attack, 0)

                    for char, (attack, health) in change_dt.items():
                        Buff(reason=ActionReason.ROUND_TABLE_BUFF, source=self.table, targets=[char],
                             health=health, attack=attack, temp=False, stack=stack).resolve()

        self.player.board.register(RoundTableBuff)
