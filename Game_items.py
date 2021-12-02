from Errors import *
class function():
    def __init__(self,name:str,function_code:int,var:int):
        self.name=name
        self.function_code=function_code
        self.var=var

    def __str__(self):
        return f'a function called {self.name} that will enact function code: {self.function_code} by {self.var} units'

    '''def enact(self,person:Player):
        if self.function_code==2:
            pass'''

class moves:
    def __init__(self, *move: function):
        self.Moves = []
        for m in move:
            self.Moves.append(m)

    def __str__(self):
        Moves = ''
        for m in self.Moves:
            Moves += f'with move {m.name} \n'
        return f'a move set with\n' \
               f'{Moves}'

    def __getitem__(self, index):
        if type(index) == int:
            c=0
            for m in self.Moves:
                if index == c:
                    return m
                else:
                    c+=1
            else:
                raise IndexError("Object Move out of Index")

        if type(index) == str:
            for m in self.Moves:
                if index.lower() == m.name.lower():
                    return m
            else:
                raise ValueError(f"{index} is not in move")

    def list_it(self)->list:
        L=[]
        for m in self.Moves:
            L.append(m.name.lower())
        return L

    def print_it(self) ->str:
        det=''
        for m in self.list_it():
            det+=m+', '
        det= det.rstrip(', ')
        return det

class item():
    def __init__(self,name:str,amnt:int,desc:str,att:moves):
        self.name=name
        self.amnt=amnt
        self.desc=desc
        self.att=att

    def __str__(self):
        return f'Item Detail\n' \
               f'Name: {self.name}\n' \
               f'Description: {self.desc}\n' \
               f'Available actions: {self.att.print_it()}\n'

    def description(self):
        return f'{self.desc}'

    def quantity(self):
        return f'{self.amnt}'

    def set_amnt(self,amnt:int):
        self.amnt=amnt

    def add_item(self,amnt:int=None):
        if amnt==None:
            self.amnt+=1
        else:
            self.amnt+=amnt

    def sub_item(self,amnt:int=None)->bool:
        if amnt == None:
            if self.check_amnt():
                self.amnt-=1
        else:
            if self.check_amnt(amnt):
                self.amnt-=amnt
            else:
                raise NotEnoughItems
        return self.check_amnt()

    def check_amnt(self,amnt:int=None)->bool:
        if amnt == None:
            if self.amnt>0:
                return True
            else:
                return False
        else:
            if amnt>=self.amnt:
                return True
            else:
                return False


class drop():
    def __init__(self,*Items:item):
        self.drop=[]
        for Item in Items:
            self.drop.append(Item)

    def __str__(self):
        Items=''
        for Item in self.drop:
            Items+=str(Item.amnt)+'x'+Item.name+', '
        Items=Items.rstrip(', ')
        return f'This drop contains the Items: {Items}'

    def content(self):
        content=''

class inventory():
    def __init__(self,*items:item):
        self.inventory=[]
        for i in items:
            self.inventory.append(i)

    def __str__(self):
        string=''
        for i in self.inventory:
            string+=i.name+' '

        return f'Inventory contains items:\n' \
               f'{string}'







