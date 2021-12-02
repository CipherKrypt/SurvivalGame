from Environment import *
from Game_items import *

class Life():
    def __init__(self,max_hp:int):
        self.max_hp=max_hp
        self.hp=max_hp

    def __str__(self) :
        return f'a Life form with Max HP: {self.max_hp} and Current HP: {self.hp}'

    def is_dead(self)-> bool:
        if self.hp<=0:
            return True
        else:
            return False

    def regenerate(self,hp_amnt):
        if self.hp +hp_amnt>self.max_hp:
            self.hp =self.max_hp
        else:
            self.hp +=hp_amnt

    def hit(self,damage)-> bool:
        if self.hp-damage <=0:
            self.hp =0
            raise DeathByDamage
        else:
            self.hp -=damage

class Exp():
    def __init__(self):
        self.xp=0
        self.next_lvl=50
        self.lvl=0

    def __str__(self):
        return f'Level: {str(self.lvl)} XP: {str(self.xp)} Next Level in: {str(self.next_lvl-self.xp)}'

    def check_xp(self):
        if self.xp==self.next_lvl:
            self.xp=0
            self.lvl+=1
            self.next_lvl*=2
        elif self.xp>self.next_lvl:
            self.xp-=self.next_lvl
            self.lvl+=1
            self.next_lvl*=2
        if self.xp<self.next_lvl:
            return
        else:
            self.check_xp()

    def add_xp(self,xp:int):
        self.xp+=xp
        self.check_xp()



class Animal(Life):
    def __init__(self,max_hp:int,animal:str,desc:str,drops:drop):
        super().__init__(max_hp)
        self.animal=animal
        self.desc=desc
        self.drops=drops

    def __str__(self):
        return super().__str__()+f' called {self.animal}.\n' \
                                 f'Description: {self.desc}\n' \
                                 f'Contains drops....\n' \
                                 f'{self.drops}'

class Tree(Life):
    def __init__(self):

class Player(Life):
    def __init__(self,max_hp,):
        super().__init__(max_hp)
        self.xp=Exp()
        self.inventory=self.premade_inventory()
        self.location:Location=self.premade_location('wild')
        self.animal:Animal=None
        self.cycle=0
        self.equiped:item=None
        self.actions=moves(self.premade_function('scout'))

    def __str__(self):
        return f'Player Details: \n'+ self.xp.__str__()+'\n' \
                f'in the location {self.location.place}'

    def equip(self,Item:item):
        self.equiped=Item

    def premade_location(self,location_name:str)->Location:
        if location_name == 'wild':
            location = Location('Wilderness', 1, 0, 10, 50, 50, 10, 0, 20, 0, 40, 0, 5, 40)
        return location

    def premade_function(self,function_name:str)-> function:
        if function_name == 'drink':
            fun= function('Drink',10,5)
        elif function_name == 'eat':
            fun= function('Eat',20,5)
        elif function_name == 'equip':
            fun= function('Equip',3,0)
        elif function_name == 'scout':
            fun = function('Scout',4,0)
        return fun

    def premade_item(self,item_name:str)-> item:
        if item_name == 'water':
            Item=item('Water',5,'A Consumable that will replenish Hydration',moves(self.premade_function('drink')))
        elif item_name == 'chicken':
            Item= item('Meat',1,'Consumable dropped by Hen and Pig that will replenish Energy',moves(self.premade_function('eat')))
        elif item_name == 'pork':
            Item = item('Meat', 2, 'Consumable dropped by Hen and Pig that will replenish Energy',moves(self.premade_function('eat')))
        elif item_name == 'axe':
            Item = item('Axe',1,'An item that can be equipped to cut down trees',moves(self.premade_function('equip')))
        return Item

    def premade_inventory(self)-> inventory:
        invent=inventory(self.premade_item('water'),self.premade_item('axe'))
        return invent

    def enact(self,func:function)-> list:
        #self.merchant,self.people,self.trees,self.berries,self.river,self.stream,self.sea,self.hen,self.pig,self.gold,self.wolf
        if func.function_code == 4:
            scouted=self.location.searchables()
            c=0
            for objects in scouted:
                if c == 0:
                    if objects:
                        pass
                if c == 1:
                    pass
                if c == 2:
                    pass





