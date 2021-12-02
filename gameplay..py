from Environment import *
from LifeForm import *
from Game_items import *

wild=Location('wild',1,0,10,50,50,10,0,20,0,40,0,5,40)
#print(wild.__str__())
Life=Life(100)
print(Life)
eat=function('Eat',2,5)
roast=function('Roast and Eat',2,10)
food=moves(eat,roast)
print(food)
Item=item('Pork',2,'Consumable that will replenish Energy',food)
Drop=drop(Item)
pig=Animal(100,'Pig','An animal with the chance to drop consumables',Drop)
player=Player(500,wild)
print(player)


