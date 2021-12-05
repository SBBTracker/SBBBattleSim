import logging

logger = logging.getLogger(__name__)


class Damage:
    def __init__(self, x, reason, source, targets, *args, **kwargs):
        self.x = x
        self.reason = reason
        self.source = source,
        self.targets = targets
        self.killed_characters = []  # This is because a nested damage effect might kill the target, comunging data

        logger.debug(f'New {self}')

        for char in targets:
            if not char.dead:
                kwargs.setdefault('stack', None)
                char.change_stats(damage=self.x, reason=self.reason, source=self.source, *args, **kwargs)
                if char.dead:
                    self.killed_characters.append(char)

    def __repr__(self):
        return f'DAMAGE: Reason: {self.reason} Amount: {self.x} Source: {self.source} Targets: {[t.pretty_print() for t in self.targets]}>>'

    def __str__(self):
        return self.__repr__()

    def resolve(self):
        logger.debug(f'RESOLVING DAMAGE FOR {self}')
        dead_characters = []
        for char in self.killed_characters:
            dead_characters.append(char)
            char.owner.graveyard.append(char)
            char.owner.characters[char.position] = None
            logger.info(f'{char.pretty_print()} died')

        logger.info(f'These are the dead characters: {dead_characters}')
        for char in sorted(dead_characters, key=lambda _char: _char.position, reverse=True):
            char('OnDeath')
