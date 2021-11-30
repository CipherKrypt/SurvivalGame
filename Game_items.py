from LifeForm import *
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

    def list_it(self)->list:
        return self.Moves

    def print_it(self) ->str:
        det=''
        for m in self.list_it():
            det+= m.name+', '
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










