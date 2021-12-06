import logging

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Echowood Dryad'
    aura = True

    _attack = 1
    _health = 1
    _level = 6
    _tribes = {Tribe.TREANT}

    def buff(self, target_character, *args, **kwargs):

        if target_character is not self:
            class EchoWoodBuff(OnBuff):
                echo_wood = self

                def handle(self, stack, summoned_characters=[], is_from_echowood=False, attack=0, health=0, damage=0,
                           reason='', temp=True, source=None, origin=None, *args, **kwargs):

                    if not origin.dead:
                        if (not temp or origin in summoned_characters) and (not is_from_echowood):
                            logger.info(f'THE ORIGIN IS {origin.pretty_print()}')

                            gold_multiplier = 2 if self.echo_wood.golden else 1

                            attack_change = max(0, gold_multiplier*attack)
                            health_change = max(0, gold_multiplier*health)

                            if attack_change > 0 or health_change > 0:
                                self.echo_wood.change_stats(
                                    attack=gold_multiplier * attack,
                                    health=gold_multiplier * health,
                                    temp=False,
                                    reason=StatChangeCause.ECHOWOOD_BUFF,
                                    source=self.manager,
                                    stack=stack,
                                    is_from_echowood=True,
                                )

            target_character.register(EchoWoodBuff, temp=True)

