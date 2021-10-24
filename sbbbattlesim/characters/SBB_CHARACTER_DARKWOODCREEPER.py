from sbbbattlesim.characters import Character


class BuffEvent(object):
    pass


class CharacterType(Character):
    name = 'Darkwood Creeper'

    class DarkwoodCreeperOnDamage(BuffEvent):
        def __call__(self, *args, **kwargs):
            pass

