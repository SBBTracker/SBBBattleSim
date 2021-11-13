from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay, OnBuff


class CharacterType(Character):
    display_name = 'Shadow Assassin'
    aura = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def buff(self, target_character):

        class ShadowAssassinOnSlay(OnSlay):
            shadow_assassin = self
            def handle(self, *args, **kwargs):
                attack_buff, health_buff = (2, 2) if self.shadow_assassin.golden else (1, 1)
                self.shadow_assassin.change_stats(attack=attack_buff, health=health_buff, temp=False,
                                                  reason=f'{self.manager} triggered a slay and is buffing {self.shadow_assassin}',source=self)
                #TODO UPDATE REASON?

        target_character.register(ShadowAssassinOnSlay, temp=True)

