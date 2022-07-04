import typing

from sbbbattlesim.action import ActionReason
from sbbbattlesim.player import Player
from sbbbattlesim.stats import StatBase


class StatType(StatBase):
    display_name = 'First Defender Position'
    hidden = True

    '''
    Example Code to get Win Rate Per First Attacker Per Attack Position
        
    win_rate_per_first_attacker_per_attack_position = {
        pid: {
            i: collections.defaultdict(int) for i in range(1, 5)
        } for pid in sim_stats.adv_stats.keys()
    }
    for result in sim_stats.results:
        first_defender_id = list(set(result.adv_stats.keys()) - set(result.first_attacker))[0]
        first_defender_position = result.adv_stats[first_defender_id]['first_defender_position']
        win_rate_per_first_attacker_per_attack_position[result.first_attacker][first_defender_position][result.win_id] += 1
    '''

    @staticmethod
    def calculate(player: Player) -> int:
        for record in player.combat_records:
            if record.reason == ActionReason.DAMAGE_WHILE_DEFENDING:
                return record.source.position
            elif record.reason == ActionReason.DAMAGE_WHILE_ATTACKING:
                break
        return -1

    @staticmethod
    def merge(stats: typing.List[typing.Union[str, int, float]]):
        return