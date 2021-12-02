from LifeForm import *
from Game_items import *

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

def game_loop():
    while True:
        c=1
        for m in player.actions.list_it():
            print(str(c),'. ',str(m).capitalize(),end='  ')
            c+=1
        print()
        try:
            ch=input('Enter>> ')
            if ch.lower().rstrip().lstrip() == 'help' or ch.lower() == '!h':
                pass
            elif ch.lower().rstrip().lstrip() in player.actions.list_it():
                pass
            else:
                print("Wrong Entry...Try Again. Enter 'help' or '!h' for help")
        except Exception as Err:
            print('Error')

game_loop()
