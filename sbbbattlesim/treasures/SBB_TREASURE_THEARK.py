from sbbbattlesim.treasures import Treasure
from sbbbattlesim.events import OnStart
from sbbbattlesim.utils import StatChangeCause


class TreasureType(Treasure):
    display_name = 'The Ark'

    def __init__(self, player):
        super().__init__(player)

        class ArkCheck(OnStart):
            ark_costs = [2, 3, 4, 5, 6]
            costs = []
            for character in self.manager.valid_characters():
                costs.append(character.cost)
            if costs in ark_costs:
                for target_character in self.manager.valid_characters():
                    target_character.change_stats(attack=12, health=12, reason=StatChangeCause.MONKEYS_PAW, source=self,
                                          temp=False)

        self.player.register(ArkCheck)
