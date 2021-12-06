class NeedHelp(Exception):
    '''When the player needs help'''

class WrongEntry(Exception):
    '''In case player entered wrong command'''

class NotAnAttribute(Exception):
    '''In case the attributes are wrong'''

class DeathByDamage(Exception):
    '''In the case that Player dies due to damage'''

class DeathByDehydration(Exception):
    '''In the case the Player didn't have enough Hydration'''

class DeathByStarvation(Exception):
    '''In the case the Player didn't have enough Energy'''

class Survived(Exception):
    '''In the case that the player survived 30 days'''