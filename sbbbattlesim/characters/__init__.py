import collections
import logging
import pkgutil
from collections import OrderedDict

logger = logging.getLogger(__name__)

logic_path = __path__


class Character:
    name = 'NO NAME SET'

    events = ()

    aura = False
    support = False

    def __init__(self, attack, health,  golden=False, position=None, keywords=[], tribes=[]):
        self.base_attack = attack
        self.base_health = health

        self.attack_bonus = 0
        self.health_bonus = 0
        self.damage = 0
        self.slay_counter = 0
        self.position = position
        self.golden = golden

        self.keywords = keywords
        self.tribes = tribes

        self.owner = None

        self._events = collections.defaultdict(list)

        for evt in self.events:
            self.register(evt(self))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'{self.name} ({self.attack}/{self.health})'

    def register(self, event):
        for event_base in event.__bases__:
            self._events[event_base].append(event)
            print(f'Registered {event_base} - {event}')

    def unregister(self, event):
        self._events.pop(event, None)

    def __call__(self, event, **kwargs):
        for evt in sorted(self._events.get(event, ()), key=lambda x: x.priority):
            evt(**kwargs)

    def buff(self, target_character):
        raise NotImplementedError(self.name)

    def dead(self):
        return self.damage > self.health

    @property
    def attack(self):
        return self.base_attack + self.attack_bonus

    @property
    def health(self):
        return self.base_health + self.health_bonus - self.damage


class Registry(object):
    characters = OrderedDict()

    def __getitem__(self, item):
        character = self.characters.get(item)
        if not character:
            character = {char.name: char for char in self.characters.values()}.get(item)

        if not character:
            class NewCharacter(Character):
                name = item
            character = NewCharacter
            # print(f'Creating Generic Character for {item}')
        return character

    def __getattr__(self, item):
        return getattr(self.characters, item)

    def __contains__(self, item):
        return item in self.characters

    def register(self, name, character):
        assert name not in self.characters, 'Character is already registered.'
        self.characters[name] = character
        print(f'Registered {name} - {character}')

    def unregister(self, name):
        self.characters.pop(name, None)

    def autoregister(self):
        for _, name, _ in pkgutil.iter_modules(logic_path):
            try:
                character = __import__(name, globals(), locals(), ['CharacterType'], 1)
                self.register(name, character.CharacterType)
            except ImportError:
                pass
            except Exception as exc:
                logger.exception('Error loading characters: {}'.format(name))

    def items(self):
        return {i.display_name: i for i in self.characters.values()}.items()


registry = Registry()
registry.autoregister()
