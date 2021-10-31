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
        p1id, p2id = list(data)
        p1data, p2data = data[p1id], data[p2id]

        def get_player(pdat, id):
            return Player(
                characters=pdat['characters'],
                treasures=pdat['treasures'],
                hero=pdat['hero'],
                hand=pdat['hand'],
                id=id,
                board=self
            )

        p1, p2 = get_player(p1data, p1id), get_player(p2data, p2id)

        self.p1 = p1
        self.p2 = p2

        self.p1.opponent = self.p2
        self.p2.opponent = self.p1
