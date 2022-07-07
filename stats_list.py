from sbbbattlesim.stats import registry as stats_registry

print('\n'.join(stat_cls.display_name for stat_cls in stats_registry.stats.values()))