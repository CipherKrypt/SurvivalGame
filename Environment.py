from Errors import *
class Location:
    def __init__(self,place:str,thirst_mult:float,o2:int,merchant:int,people:int,trees:int,berries:int,water_source:int,hen:int,pig:int,gold:int,wolf:int):
        self.place=place
        self.thirst_mult=thirst_mult
        self.o2=o2
        self.merchant=merchant
        self.people=people
        self.trees=trees
        self.berries=berries
        self.water_source=water_source
        self.hen=hen
        self.pig=pig
        self.gold=gold
        self.wolf=wolf

    def __str__(self):
        return f'This {self.place} has....\n' \
               f'a x{self.thirst_mult} multiple of increasing thirst\n' \
               f'a x{self.o2} multiple of decreasing your O2\n' \
               f'a {self.merchant}% chance of meeting a merchant\n' \
               f'a {self.people}% chance of meeting a person\n' \
               f'a {self.trees}% chance of finding a tree\n' \
               f'a {self.berries}% chance of finding healing berries\n' \
               f'a {self.water_source}% chance of finding a water source\n' \
               f'a {self.hen}% chance of finding a hen\n' \
               f'a {self.pig}% chance of finding a pig\n' \
               f'a {self.gold}% chance of finding gold\n' \
               f'a {self.wolf}% chance of encountering a wolf'


    """"Searchables returns the chance of finding each attribute as a list """
    def searchables(self)-> list:
        return [self.merchant,self.people,self.trees,self.berries,self.water_source,self.hen,self.pig,self.gold,self.wolf]

    """Search returns if the player was able to find the certain attribute as boolean values a
     and puts it in a List after which we can traverse the list and do the needful."""
    def search(self) ->list:
        from random import randint
        search_result=[]
        for items in self.searchables():
            chance=randint(0,100)
            if chance<=items:
                search_result.append(True)
            else:
                search_result.append(False)

        return search_result

    """Decreases the chance of finding a specific or all of the attributes by a fixed amnt 
    on the bases of the given string."""
    def decrease_attribute(self,att:str,amnt=5):
        if att=='th':
            if self.decrease(self.thirst_mult):
                self.thirst_mult-=0.5
        elif att=='o':
            if self.decrease(self.o2):
                self.o2-=0.5
        elif att=='m':
            if self.decrease(self.merchant):
                self.merchant-=amnt
        elif att=='pe':
            if self.decrease(self.people):
                self.people-=amnt
        elif att=='t':
            if self.decrease(self.trees):
                self.trees-=amnt
        elif att=='b':
            if self.decrease(self.berries):
                self.berries-=amnt
        elif att=='wa':
            if self.decrease(self.water_source):
                self.water_source-=amnt
        elif att=='h':
            if self.decrease(self.hen):
                self.hen-=amnt
        elif att=='p':
            if self.decrease(self.pig):
                self.pig-=amnt
        elif att=='g':
            if self.decrease(self.gold):
                self.gold-=amnt
        elif att=='w':
            if self.decrease(self.wolf):
                self.wolf-=amnt
        elif att=='all':
            for attribute in ['th','o','m','pe','t','b','wa','h','p','g','w']:
                self.decrease_attribute(attribute)
        else:
            raise NotAnAttribute #raise this error if the wrong attribute string was entered

    """Check if the given attribute is 0 or not"""
    def decrease(self,attribute:int):
        if attribute!=0:
            return True

    """Decreases the chance of finding a specific or all of the attributes by a fixed amnt 
        on the bases of the given string."""
    def increase_attribute(self,att:str,amnt=5):
        if att=='th':
            self.thirst_mult +=0.5
        elif att=='o':
            self.o2 +=0.5
        elif att=='m':
            if self.increase(self.merchant):
                self.merchant +=amnt
        elif att=='pe':
            if self.increase(self.people):
                self.people +=amnt
        elif att=='t':
            if self.increase(self.trees):
                self.trees +=amnt
        elif att=='b':
            if self.increase(self.berries):
                self.berries +=amnt
        elif att=='wa':
            if self.increase(self.water_source):
                self.water_source +=amnt
        elif att=='h':
            if self.increase(self.hen):
                self.hen +=amnt
        elif att=='p':
            if self.increase(self.pig):
                self.pig +=amnt
        elif att=='g':
            if self.increase(self.gold):
                self.gold +=amnt
        elif att=='w':
            if self.increase(self.wolf):
                self.wolf +=amnt
        elif att=='all':
            for attribute in ['th','o','m','pe','t','b','wa','h','p','g','w']:
                self.increase_attribute(attribute)
        else:
            raise NotAnAttribute #raise this error if the wrong attribute string was entered

    """Checks if the chance of finding an attribute is 100% or not and returns boolean value"""
    def increase(self,attribute:int)-> bool:
        if attribute!=100:
            return True
