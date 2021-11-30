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


