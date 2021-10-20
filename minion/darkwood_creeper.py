from minion import Minion


class BuffEvent(object):
    pass


class MinionType(Minion):
    name = 'Darkwood Creeper'

    class DarkwoodCreeperOnDamage(BuffEvent):
