import collections


class SSBBSEvent:
    priority = 0
    def __init__(self, character):
        self.character = character

    def __call__(self, *args, **kwargs):
        pass


class Start(SSBBSEvent):
    '''Start of brawl'''


class Death(SSBBSEvent):
    '''A character'''


class Buff(SSBBSEvent):
    '''A character is buffed'''


class Support(SSBBSEvent):
    '''A character is supported'''


class Aura(SSBBSEvent):
    '''A character is buffed by an Aura'''


class Slay(SSBBSEvent):
    '''A slay is triggered'''


class Spawn(SSBBSEvent):
    '''A character is summoned'''


class Spell(SSBBSEvent):
    '''A spell is cast'''


class Attack(SSBBSEvent):
    '''An attacking character attacks'''


class Defend(SSBBSEvent):
    '''A defending character is attacked'''


class DamagedAndSurvived(SSBBSEvent):
    '''A character gets damaged and doesn't die'''
