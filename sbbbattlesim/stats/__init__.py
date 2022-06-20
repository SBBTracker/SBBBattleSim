import collections
import logging
import pkgutil
import typing
from collections import OrderedDict

from sbbbattlesim.player import Player

logger = logging.getLogger(__name__)

logic_path = __path__


def calculate_adv_stats(player: Player):
    calculated_stats = {}

    for slug, stat_cls in registry.stats.items():
        value = stat_cls.calculate(player)
        if value:
            calculated_stats[slug] = value

    return calculated_stats


def finalize_adv_stats(results: typing.List['CombatStats']) -> typing.Dict[str, typing.Dict[str, str]]:
    merged_stats = {}  # {pid: {sid: StatType}}
    for combat_result in results:
        for pid, stats in combat_result.adv_stats.items():
            if pid not in merged_stats:
                merged_stats[pid] = collections.defaultdict(list)
            for sid, s in stats.items():
                merged_stats[pid][sid].append(s)

    finalize_stats = {}  # {pid: {stat display name: stat pretty print}}
    for pid, stats in merged_stats.items():
        player_stats = {}
        for sid, stat_list in sorted(stats.items(), key=lambda sids: sids[1]):
            stat_cls = registry.stats[sid]
            player_stats[stat_cls.display_name] = stat_cls.display_format.format(stat_cls.merge(stat_list))
        finalize_stats[pid] = player_stats

    return finalize_stats


class StatBase:
    id: str = ''
    display_name: str = ''
    display_format: str = ''

    @staticmethod
    def calculate(player: Player) -> int:
        raise NotImplementedError

    @staticmethod
    def merge(stats: typing.List['StatBase']):
        raise NotImplementedError

    @classmethod
    def valid(cls):
        if not all((
            isinstance(cls.display_name, str), cls.display_name,
            isinstance(cls.display_format, str), cls.display_format
        )):
            raise ValueError


class Registry(object):
    stats = OrderedDict()
    auto_registered = False

    def __getitem__(self, item):
        return self.stats.get(item)

    def __getattr__(self, item):
        return getattr(self.stats, item)

    def __contains__(self, item):
        return item in self.stats

    def register(self, name, stat):
        assert name not in self.stats, name
        stat.id = name
        self.stats[name] = stat
        logger.debug(f'Registered {name} - {stat}')

    def autoregister(self):
        if self.auto_registered:
            return
        self.auto_registered = True

        for _, name, _ in pkgutil.iter_modules(logic_path):
            stat = __import__(name, globals(), locals(), ['StatType'], 1)
            if name in self.stats or stat.StatType.valid():
                raise NotImplementedError
            self.register(name, stat.StatType)


registry = Registry()