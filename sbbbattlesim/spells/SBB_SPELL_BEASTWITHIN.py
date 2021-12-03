import logging

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.events import OnDeath
from sbbbattlesim.spells import NonTargetedSpell


logger = logging.getLogger(__name__)


class SpellType(NonTargetedSpell):
    display_name = '''Cat's Call'''
    _level = 4

    def cast(self, player, *args, **kwargs):
        front_row_lambda = lambda char: char.position in (1, 2, 3, 4)

        class CatsCallOnDeath(OnDeath):
            last_breath = False
            priority = 1000
            def handle(self, *args, **kwargs):
                logger.debug(f'CATS CALL CHECK {len(player.valid_characters(_lambda=front_row_lambda)) == 0}')
                if len(player.valid_characters(_lambda=front_row_lambda)) == 0:
                    for pos in (1, 2, 3, 4):
                        cat = character_registry['Cat'](
                            self.manager.owner,
                            pos,
                            1,
                            1,
                            golden=False,
                            keywords=[],
                            tribes=['evil', 'animal'],
                            cost=1
                        )
                        player.summon_from_different_locations([cat])

        for char in player.valid_characters(_lambda=front_row_lambda):
            char.register(CatsCallOnDeath, temp=False)
