from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'Monkey\'s Paw'

    # todo make enum for stateful effects

    def __init__(self, player):
        super().__init__(player)

        class MonkeysPawCheck(OnStart):
            if self.manager.valid_characters() <= 6:
                player.stateful_effects['MONKEY_PAW'] = True
            else:
                player.stateful_effects['MONKEY_PAW'] = False
        self.player.register(MonkeysPawCheck)

    def buff(self, target_character):
        if self.player.stateful_effects['MONKEY_PAW']:

            target_character.change_stats(attack=6, health=6, reason=StatChangeCause.MONKEYS_PAW, source=self, temp=True)
