class SSBBSEvent:
    def __init__(self, minion):
        self.minion = minion
    '''Base SSBBS Event'''


class LastBreathEvent(SSBBSEvent):
    '''A Death Event'''


class BuffsEvent(SSBBSEvent):
    '''A Support Event'''


class SlayEvent(SSBBSEvent):
    '''A Slay Event'''