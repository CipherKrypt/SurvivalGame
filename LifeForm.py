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
            return self.is_dead()
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

class Player(Life):
    def __init__(self,max_hp,loc:Location,animal:Animal=None):
        super().__init__(max_hp)
        self.xp=Exp()
        self.inventory:inventory=
        self.location=loc
        self.animal=animal

    def __str__(self):
        return f'Player Details: \n'+ self.xp.__str__()+'\n' \
                f'in the location {self.location.place}'



