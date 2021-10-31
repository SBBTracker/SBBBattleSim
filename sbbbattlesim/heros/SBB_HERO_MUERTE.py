from sbbbattlesim.events import OnLastBreath
from sbbbattlesim.heros import Hero


class MuerteLastBreatBuff(OnLastBreath):
    def handle(self, *args, **kwargs):
        last_breather = kwargs['last_breather']
        if not self.manager.owner.stateful_effects.get('Muerte_Proc', False):
            # TODO only handle 1 trigger
            last_breather('OnDeath', *args, **kwargs)
            self.manager.owner.stateful_effects['Muerte_Proc'] = True


class HeroType(Hero):
    display_name = 'Muerte'
    aura = True

    # NOTE question: does this trigger the first one, or the rightmost one that triggers in the same stack?
    def buff(self, target_character):
        if 'evil' in target_character.tribes:
            target_character.register(MuerteLastBreatBuff, temp=True)