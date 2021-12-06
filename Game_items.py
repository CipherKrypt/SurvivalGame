from Errors import *

class function():
    def __init__(self,name:str,function_code:int,var:int):
        self.name=name
        self.function_code=function_code
        self.var=var

    def __str__(self):
        return f'a function called {self.name} that will enact function code: {self.function_code} by {self.var} units'

    def set_var(self,amnt:int):
        self.var=amnt

class moves:
    def __init__(self, *move: function or None):
        self.Moves = []
        for m in move:
            self.Moves.append(m)

    def __str__(self):
        Moves = ''
        if self.Moves == None:
            Moves+= f'with no moves'
        else:
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

    def list_it(self,is_item=False)->list:
        L=[]
        if is_item:
            if self.Moves == None:
                pass
            else:
                L.append(self.Moves[0].name)
            L.append(function('return',8,0).name)
        else:
            try:
                for m in self.Moves:
                    L.append(m.name.lower())
            except:
                L.append('None')
        return L

    def print_it(self,is_item=False) ->str:
        det=''
        for m in self.list_it(is_item):
            det+=m+'   '
        det= det.rstrip('   ')
        return det

class item():
    def __init__(self,name:str,amnt:int,desc:str,att:moves or None,cost:int):
        self.name=name
        self.amnt: int =amnt
        self.desc=desc
        self.att:moves or None =att
        self.cost:int = cost

    def __str__(self):
        Att=''
        try:
            if len(self.att.list_it())>1:
                for i in range(1,len(self.att.list_it())):
                    Att+=self.att[i].name+' | '
                Att.rstrip(' | ')
            else:
                Att = 'No Attributes'
        except:
            Att='No Attributes'

        if self.att != None:
            att = self.att.print_it(True)
        else:
            att = 'Nothing'
        return f'Item Detail\n' \
               f'Name: {self.name}\n' \
               f'Amount: {str(self.amnt)}\n' \
               f'Description: {self.desc}\n' \
               f'Attribute: {Att}\n' \
               f'Available actions: {att}\n'

    def description(self):
        print(f'{self.desc}')

    def quantity(self):
        return f'{str(self.amnt)}'

    def set_amnt(self,n:int):
        self.amnt = n

    def add_item(self,amnt:int=None):
        if amnt==None:
            self.amnt+=1
        else:
            self.amnt+=amnt

    def sub_item(self,amnt:int=None)->bool:
        if amnt == None:
            if self.check_amnt():
                n=self.amnt
                self.amnt=n-1
                return True
            else:
                return False
        else:
            if self.check_amnt(amnt):
                n=self.amnt
                self.amnt=n-amnt
                return True
            else:
                return False

    def check_amnt(self,amnt:int=None)->bool:
        if amnt == None:
            if self.amnt>0:
                return True
            else:
                return False
        else:
            if amnt<=self.amnt:
                return True
            else:
                return False

class inventory():
    def __init__(self,*items:item or None):
            self.inventory=[]
            for i in items:
                self.inventory.append(i)

    def __str__(self):
        string=''
        for i in self.inventory:
            string+=str(i.name)+' '

        return f'Inventory contains items:\n' \
               f'{string}'

    def __getitem__(self, index):
        if type(index) == int:
            c=0
            for i in self.inventory:
                if index == c:
                    return i
                else:
                    c+=1
            else:
                raise IndexError("Object Inventory out of Index")
        if type(index) == str:
            for m in self.inventory:
                if index.lower() == m.name.lower():
                    return m
            else:
                raise ValueError(f"{index} is not in Inventory")

    def list_inv(self)->list:
        L=[]
        for i in self.inventory:
            L.append(i)
        return L

    def add_inv(self,items:item):
        c=0
        for i in self.inventory:
            if i.name.lower() == items.name.lower():
                amnt=items.amnt
                total=i.amnt
                total+=amnt
                i.set_amnt(total)
                print(f'{items.amnt}x{items.name} added to inventory\n')
                return
            else:
                c+=1
        else:
            self.inventory.append(items)
            print(f'New Item {items.name} added to inventory\n'
                  f'{items.desc}\n')
            print(f'{items.amnt}x{items.name} added to inventory\n')

    def use_item(self,itim:str,amnt=1)->bool:
        try:
            for m in self.inventory:
                print(itim.lower(),m.name.lower())
                if itim.lower() == m.name.lower():
                    print(m)
                    if m.sub_item(amnt):
                        if m.amnt == 0:
                            print(self.inventory)
                            self.inventory.remove(m)
                        return True
                    else:
                        return False

            else:
                return False
        except:
            return False

    def content(self):
        content=[]
        try:
            for item in self.inventory:
                content.append(item.name.lower)
        except:
            return []
        return content

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
        for item in self.drop:
            content+=item.name.capitalize()+' and '
        content = content.rstrip('and ')
        return content

    def collect(self,player_inv:inventory):
        for item in self.drop:
            player_inv.add_inv(item)


class shop():
    def __init__(self,*items:item):
        self.Shop =list()
        for i in items:
            self.Shop.append(i)
            
    def __str__(self):
        string=f"Merchant's Trinkets\n" \
               f"0. Exit\n"
        for items in self.list_it():
            string+=f"{items}\n"
        return string
        
    def __getitem__(self, index):
        if type(index) == int:
            c=0
            for i in self.Shop:
                if index == c:
                    return i
                else:
                    c+=1
            else:
                raise IndexError("Object Shop out of Index")
        if type(index) == str:
            for i in self.Shop:
                if index.lower() == i.name.lower():
                    return i
            else:
                raise ValueError(f"{index} is not in Inventory")
        
    def list_it(self):
        L=[]
        c = 1
        for i in self.Shop:
            L.append(f"{c}. {i.name} : {i.desc}")
            c+=1
        return L


