import logging

logger = logging.getLogger(__name__)


class Damage:
    def __init__(self, x, reason, source, targets):
        self.x = x
        self.reason = reason
        self.source = source,
        self.targets = targets

        logger.debug(f'New Damage Instance ({x}, {reason}, {source}, {targets})')

        for char in self.targets:
            char.change_stats(damage=self.x, reason=self.reason, source=self.source)

    def resolve(self):
        logger.debug(f'RESOLVING DAMAGE FOR {self}')
        dead_characters = []
        for char in self.targets:
            if char.dead:
                dead_characters.append(char)
                char.owner.graveyard.append(char)
                char.owner.characters[char.position] = None
                logger.info(f'{char} died')

        for char in sorted(dead_characters, key=lambda _char: _char.position, reverse=True):
            char('OnDeath')
