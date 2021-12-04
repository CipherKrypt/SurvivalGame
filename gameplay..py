from LifeForm import *
from Errors import *

player=Player(500)
'''
#print(wild.__str__())
Life=Life(100)
#print(Life)
eat=function('Eat',2,5)
roast=function('Roast and Eat',2,10)
food=moves(eat,roast)
#print(food)
Item=item('Pork',2,'Consumable that will replenish Energy',food)
Drop=drop(Item)
pig=Animal(100,'Pig','An animal with the chance to drop consumables',Drop)
player=Player(500,wild)
print(player)
#print(player)
'''
def get_ch(player:Player):
    print(player.actions.print_it())
    ch = input('Enter>> ')
    ch = ch.lower().rstrip().lstrip()
    if == 'help' or ch.lower() == '!h':
        raise N
    elif ch in player.actions.print_it():
        pass
    else:

def game_loop():
    while True:
        try:

                print("Wrong Entry...Try Again. Enter 'help' or '!h' for help")
        except Exception as Err:
            print('Error')

game_loop()
