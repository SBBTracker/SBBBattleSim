from characters import Character


class BuffEvent(object):
    pass


class CharacterType(Character):
    name = 'Darkwood Creeper'

    class DarkwoodCreeperOnDamage(BuffEvent):
