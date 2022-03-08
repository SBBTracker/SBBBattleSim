import logging
import random

from sbbbattlesim.combat import fight
from sbbbattlesim.events import EventManager
from sbbbattlesim.player import Player

logger = logging.getLogger(__name__)


class Board(EventManager):
    def __init__(self, data):
        super().__init__()
        logger.debug(data)
        assert isinstance(data, dict), data
        p1id, p2id = list(data)
        p1data, p2data = data[p1id], data[p2id]

        p1, p2 = Player(id=p1id, board=self, **p1data), Player(id=p2id, board=self, **p2data)

        self.p1 = p1
        self.p2 = p2

        self.p1.opponent = self.p2
        self.p2.opponent = self.p1

        self.winner = None
        self.loser = None

        self.history = []

    def get_player(self, id):
        if self.p1.id == id:
            return self.p1
        if self.p2.id == id:
            return self.p2

    def fight(self, limit=-1):
        attacker, defender = who_goes_first(self.p1, self.p2)
        logger.debug('********************SETTING UP COMBAT')
        self('OnSetup')
        logger.debug('********************STARTING COMBAT')
        self('OnStart')
        self.winner, self.loser = fight(attacker, defender, limit=limit)
        return self.winner, self.loser

    def to_state(self):
        return {
            self.p1.id: self.p1.to_state(),
            self.p2.id: self.p2.to_state()
        }


def who_goes_first(p1, p2):
    p1cnt = _who_goes_first(p1)
    p2cnt = _who_goes_first(p2)

    if p1cnt > p2cnt:
        attacking, defending = p1, p2
    elif p2cnt > p1cnt:
        defending, attacking = p1, p2
    else:
        attacking, defending = random.sample((p1, p2), 2)

    return attacking, defending


def _who_goes_first(player):
    HERMES_BOOTS = '''SBB_TREASURE_HERMES'BOOTS'''
    TIGER = '''SBB_HERO_THECOLLECTOR'''
    MIMIC = '''SBB_TREASURE_TREASURECHEST'''
    DRAC = '''SBB_HERO_DRACULA'''

    cnt = 0
    if player.hero.id == DRAC:
        cnt += 1

    if player.treasures.get(HERMES_BOOTS):
        cnt += 1
        if player.treasures.get(MIMIC):
            cnt += 1
        if player.hero.id == TIGER:
            cnt += 1

    return cnt
