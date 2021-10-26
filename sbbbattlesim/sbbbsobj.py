from sbbbattlesim.events import EventManager


class SBBBSObject(EventManager):
    name = ''
    aura = False
    events = ()

    def buff(self, target_character):
        raise NotImplementedError(self.name)