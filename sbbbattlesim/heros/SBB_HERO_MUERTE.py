from sbbbattlesim.events import OnLastBreath, OnDeath
from sbbbattlesim.heros import Hero



class HeroType(Hero):
    display_name = 'Muerte'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.triggered = False

    def buff(self, target_character):
        if self.triggered:
            return

        class MeurteDoubleLastBreath(OnDeath):
            meurte = self
            priority = -999
            last_breath = False
            def handle(self, *args, **kwargs):
                if self.meurte.triggered:
                    return

                last_breaths = [evt for evt in self.manager.get('OnDeath') if evt.last_breath]
                if last_breaths:
                    self.meurte.triggered = True
                    react, rargs, rkwargs = last_breaths[-1](*args, **kwargs)
                    self.manager(react, *rargs, **rkwargs)

        target_character.register(MeurteDoubleLastBreath)
