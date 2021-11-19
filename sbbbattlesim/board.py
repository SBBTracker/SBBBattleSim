import random
import time
import traceback
from copy import deepcopy

from sbbbattlesim.events import EventManager
from sbbbattlesim.player import Player
from sbbbattlesim.combat import fight_initialization
import logging

logger = logging.getLogger(__name__)

class Board(EventManager):
    def __init__(self, data):
        super().__init__()
        assert isinstance(data, dict)
        logger.debug(data)
        p1id, p2id = list(data)
        p1data, p2data = data[p1id], data[p2id]

        p1, p2 = Player(id=p1id, board=self, **p1data), Player(id=p2id, board=self, **p2data)

        self.p1 = p1
        self.p2 = p2

        self.p1.opponent = self.p2
        self.p2.opponent = self.p1

    def get_player(self, id):
        if self.p1.id == id:
            return self.p1
        if self.p2.id == id:
            return self.p2

    def fight(self, limit=None):
        HERMES_BOOTS = '''SBB_TREASURE_HERMES'BOOTS'''
        # Determine Setup and Turn Order
        if self.p1.treasures.get(HERMES_BOOTS) and not self.p2.treasures.get(HERMES_BOOTS):
            attacking, defending = self.p1, self.p2
        elif self.p2.treasures.get(HERMES_BOOTS) and not self.p1.treasures.get(HERMES_BOOTS):
            attacking, defending = self.p2, self.p1
        else:
            attacking, defending = random.sample((self.p1, self.p2), 2)

        return fight_initialization(attacker=attacking, defender=defending, limit=limit, board=self)
