import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class EchoWoodBuff(OnBuff):
    def handle(self, stack, summoned_characters=[], is_from_echowood=False, attack=0, health=0, damage=0,
               reason='', temp=True, source=None, *args, **kwargs):

        if not self.manager.dead:
            if (not temp or self.manager in summoned_characters) and (not is_from_echowood):

                gold_multiplier = 2 if self.echo_wood.golden else 1

                attack_change = max(0, gold_multiplier * attack)
                health_change = max(0, gold_multiplier * health)

                if attack_change > 0 or health_change > 0:
                    Buff(reason=ActionReason.ECHOWOOD_BUFF, source=self.manager, targets=[self.echo_wood],
                         attack=gold_multiplier * attack, health=gold_multiplier * health,
                         temp=False, stack=stack, is_from_echowood=True).resolve()


class CharacterType(Character):
    display_name = 'Echowood Dryad'
    aura = True

    _attack = 1
    _health = 1
    _level = 6
    _tribes = {Tribe.TREANT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura_buff = Aura(source=self, echo_wood=self, event=EchoWoodBuff, _lambda=lambda char: char is not self)

    def buff(self, target_character, *args, **kwargs):
        self.aura_buff.execute(target_character)
