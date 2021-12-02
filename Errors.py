class NotAnAttribute(Exception):
    '''In case the attributes are wrong'''

class NotEnoughItems(Exception):
    '''In the case that Player doesn't have enough items for an action'''

class DeathByDamage(Exception):
    '''In the case that Player dies'''