class SSBBSEvent:
    def __init__(self, character):
        self.character = character
    '''Base SSBBS Event'''


class LastBreathEvent(SSBBSEvent):
    '''A Death Event'''


class BuffsEvent(SSBBSEvent):
    '''A Support Event'''


class SlayEvent(SSBBSEvent):
    '''A Slay Event'''