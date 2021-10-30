import logging
import pkgutil
from collections import OrderedDict
from sbbbattlesim.sbbbsobj import SBBBSObject

logger = logging.getLogger(__name__)

logic_path = __path__


class Character(SBBBSObject):
    support = False

    def __init__(self, owner, position, attack, health, golden, keywords, tribes, cost):
        super().__init__()
        self.owner = owner

        self.position = position
        self._base_attack = attack
        self._base_health = health
        self.golden = golden
        self.keywords = keywords
        self.tribes = tribes
        self.cost = cost

        self.attack_bonus = 0
        self.health_bonus = 0
        self._damage = 0
        self.slay_counter = 0
        self.dead = False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'''{self.display_name} ({self.attack}/{self.health})'''

    @property
    def attack(self):
        return self.base_attack + self.attack_bonus

    @property
    def health(self):
        return self.base_health + self.health_bonus - self.damage

    @property
    def base_health(self):
        return self._base_health

    @base_health.setter
    def base_health(self, value):
        if value > self.base_health:
            self('OnBuff', health_buff=value-self._base_health)
        self._base_health = value

    @property
    def base_attack(self):
        return self._base_attack

    @base_attack.setter
    def base_attack(self, value):
        if value > self.base_attack:
            self('OnBuff', attack_buff=value-self._base_attack)
        self._base_attack = value

    def max_health(self):
        return self.base_health + self.health_bonus

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value
        if self.health <= 0:
            self.dead = True
            

class Registry(object):
    characters = OrderedDict()

    def __getitem__(self, item):
        character = self.characters.get(item)
        if not character:
            character = {char.display_name: char for char in self.characters.values()}.get(item)

        if not character:
            class NewCharacter(Character):
                display_name = item

            character = NewCharacter
            # print(f'Creating Generic Character for {item}')

        # Set the id for reference
        character.id = item

        return character

    def __getattr__(self, item):
        return getattr(self.characters, item)

    def __contains__(self, item):
        return item in self.characters

    def register(self, name, character):
        assert name not in self.characters, 'Character is already registered.'
        self.characters[name] = character
        logger.debug(f'Registered {name} - {character}')

    def unregister(self, name):
        self.characters.pop(name, None)

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                character = __import__(name, globals(), locals(), ['CharacterType'], 1)
                self.register(name, character.CharacterType)
            except ImportError as e:
                pass
            except Exception as exc:
                logger.exception('Error loading characters: {}'.format(name))

    def items(self):
        return {i.display_name: i for i in self.characters.values()}.items()


registry = Registry()
registry.autoregister()
