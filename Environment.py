from Errors import *
class Location:
    def __init__(self,place:str,thirst_mult:int,o2:int,merchant:int,people:int,trees:int,berries:int, river:int, stream:int, sea:int,hen:int,pig:int,gold:int,wolf:int):
        self.place=place
        self.thirst_mult=thirst_mult
        self.o2=o2
        self.merchant=merchant
        self.people=people
        self.trees=trees
        self.berries=berries
        self.river=river
        self.stream=stream
        self.sea=sea
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
               f'a {self.river}% chance of finding a river\n' \
               f'a {self.stream}% chance of finding a stream\n' \
               f'a {self.sea}% chance of finding a sea\n' \
               f'a {self.hen}% chance of finding a hen\n' \
               f'a {self.pig}% chance of finding a pig\n' \
               f'a {self.gold}% chance of finding gold\n' \
               f'a {self.wolf}% chance of encountering a wolf'

    def searchables(self)-> list:
        return [self.merchant,self.people,self.trees,self.berries,self.river,self.stream,self.sea,self.hen,self.pig,self.gold,self.wolf]

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

    def decrease_attribute(self,att:str):
        if att=='th':
            if self.decrease(self.thirst_mult):
                self.thirst_mult-=0.5
        elif att=='o':
            if self.decrease(self.o2):
                self.o2-=0.5
        elif att=='m':
            if self.decrease(self.merchant):
                self.merchant-=5
        elif att=='pe':
            if self.decrease(self.people):
                self.people-=5
        elif att=='t':
            if self.decrease(self.trees):
                self.trees-=5
        elif att=='b':
            if self.decrease(self.berries):
                self.berries-=5
        elif att=='r':
            if self.decrease(self.river):
                self.river-=5
        elif att=='st':
            if self.decrease(self.stream):
                self.stream-=5
        elif att=='s':
            if self.decrease(self.sea):
                self.sea-=5
        elif att=='h':
            if self.decrease(self.hen):
                self.hen-=5
        elif att=='p':
            if self.decrease(self.pig):
                self.pig-=5
        elif att=='g':
            if self.decrease(self.gold):
                self.gold-=5
        elif att=='w':
            if self.decrease(self.wolf):
                self.wolf-=5
        elif att=='all':
            for attribute in ['th','o','m','pe','t','b','r','st','s','h','p','g','w']:
                self.decrease_attribute(attribute)
        else:
            raise NotAnAttribute

    def decrease(self,attribute:int):
        if attribute!=0:
            return True
    def increase_attribute(self,att:str):
        if att=='th':
            self.thirst_mult +=0.5
        elif att=='o':
            self.o2 +=0.5
        elif att=='m':
            if self.increase(self.merchant):
                self.merchant +=5
        elif att=='pe':
            if self.increase(self.people):
                self.people +=5
        elif att=='t':
            if self.increase(self.trees):
                self.trees +=5
        elif att=='b':
            if self.increase(self.berries):
                self.berries +=5
        elif att=='r':
            if self.increase(self.river):
                self.river +=5
        elif att=='st':
            if self.increase(self.stream):
                self.stream +=5
        elif att=='s':
            if self.increase(self.sea):
                self.sea +=5
        elif att=='h':
            if self.increase(self.hen):
                self.hen +=5
        elif att=='p':
            if self.increase(self.pig):
                self.pig +=5
        elif att=='g':
            if self.increase(self.gold):
                self.gold +=5
        elif att=='w':
            if self.increase(self.wolf):
                self.wolf +=5
        elif att=='all':
            for attribute in ['th','o','m','pe','t','b','r','st','s','h','p','g','w']:
                self.increase_attribute(attribute)
        else:
            raise NotAnAttribute

    def increase(self,attribute:int):
        if attribute!=100:
            return True
