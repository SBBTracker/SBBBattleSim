from sbbbattlesim.events import OnLastBreath
from sbbbattlesim.heros import Hero


class MuerteLastBreatBuff(OnLastBreath):
    def handle(self, *args, **kwargs):
        last_breather = kwargs['last_breather']
        if not getattr(self.manager.owner, 'Meurte_Proc', False):
            # TODO only handle 1 trigger
            last_breather('OnDeath', *args, **kwargs)
            setattr(self.manager.owner, 'Meurte_Proc', True)


class HeroType(Hero):
    display_name = 'Muerte'
    aura = True

    def buff(self, target_character):
        if 'evil' in target_character.tribes:
            target_character.register(MuerteLastBreatBuff, temp=True)