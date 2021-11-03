from sbbbattlesim.spells import TargetedSpell


class SpellType(TargetedSpell):
    display_name = 'Magic Research'
    spell_type = ()

    def cast(self, target, *args, **kwargs):
        target.change_stats(health=1, attack=1, temp=False, reason=f'{self} buff')