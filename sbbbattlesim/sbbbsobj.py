from sbbbattlesim.events import EventManager


class SBBBSObject(EventManager):
    display_name = ''
    id = ''
    aura = False

    def buff(self, target_character):
        raise NotImplementedError(self.display_name)