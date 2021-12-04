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
def main_menu():
    print('Main Menu')

def game_loop():
    while True:
        try:
            player.actions = moves(player.premade_function('scout'),player.premade_function('inventory'))
            player.get_ch()
            player.cycle()
        except Exception as Err:
            if Err == NeedHelp:
                player.help()
            elif Err == WrongEntry:
                print('Invalid Entry...Try again')
            elif Err == DeathByDamage or Err == DeathByDehydration or Err == DeathByStarvation:
                player.game_over(Err)
                main_menu()
            else:
                print(Err)

game_loop()
