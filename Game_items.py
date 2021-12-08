from Errors import *
"""Class function to hold objects with function name, function code for the program to know what action to take
and a variable holder to know by how much the action should be done"""
class function():
    def __init__(self,name:str,function_code:int,var:int):
        self.name=name
        self.function_code=function_code
        self.var=var

    def __str__(self):
        return f'a function called {self.name} that will enact function code: {self.function_code} by {self.var} units'

    def set_var(self, amnt: int):
        self.var = amnt

"""A class moves that will hold a list of functions that can then be assigned to an item in the game."""

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



    def __getitem__ (self, index):
        """A built in definition to make the object subscriptable... that is be able to index it using square brackets"""
        """In my definition I allowed it to be indexed using integers and string containing the name of the function."""
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
        """Iterates to the object and returns a list of function names held by the object"""
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
        """Returns a string of the functions with 3 spaces between which can be used in game to
        print the possible functions that the player can undertake"""
        det=''
        for m in self.list_it(is_item):
            det+=m+'   '
        det= det.rstrip('   ')
        return det


class item():
    """The class item to hold objects that act as items in the game
    it has name, amount of items, it's description, and attributes or a list of moves that holds it's many function"""
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
        """Returns a string containing the description of the item"""
        print(f'{self.desc}')


    def quantity(self):
        "Returns a string containing the quantity of the item"
        return f'{str(self.amnt)}'


    def set_amnt(self,n:int):
        """Allows to set the quantity of the object by a value"""
        self.amnt = n


    def add_item(self,amnt:int=None):
        """Allows to add to the item's quantity, by default it will add 1"""
        if amnt==None:
            self.amnt+=1
        else:
            self.amnt+=amnt


    def sub_item(self,amnt:int=1)->bool:
            """Allows to subtract the quantity, by default it will subtract 1. Will return a boolean value depending on
            if the subtraction was possible."""
            if self.check_amnt(amnt):
                n=self.amnt
                self.amnt=n-amnt
                return True
            else:
                return False

    def check_amnt(self,amnt:int=1)->bool:
            """Function to check if the quantity can be subtracted by an amount or not
            and returns a boolean value regarding the same"""
            if amnt<=self.amnt:
                return True
            else:
                return False


class inventory():
    """class inventory to hold the all the items the player as a list of item objects"""
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
        """built in defined function to make the inventory subscriptable"""
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
        """A function that will return the items in the inventory as a lsit"""
        L=[]
        for i in self.inventory:
            L.append(i)
        return L


    def add_inv(self,items:item):
        """function to add an item to inventory...if a new item it will show a message describing the item else just
        add to the quantity of pre existing item."""
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
        """Function to use an item in the inventory by an amount that will automatically deduct from the item quantity"""
        try:
            for m in self.inventory:
                if itim.lower() == m.name.lower():
                    if m.sub_item(amnt):
                        return True
                    else:
                        return False

            else:
                return False
        except:
            return False


    def content(self)-> list:
        """returns a list of item names in the inventory as a list"""
        content=[]
        try:
            for item in self.inventory:
                content.append(item.name.lower)
        except:
            return []
        return content


class drop():
    """class drop that contains a list of items that can be assigned to an Animal to be dropped when hunted or attacked"""
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


    def content(self)->str:
        """Function to return a string of the drops contents"""
        content=''
        for item in self.drop:
            content+=item.name.capitalize()+' and '
        content = content.rstrip('and ')
        return content


    def collect(self,player_inv:inventory):
        """A function for the items in the drop to be added to the player's inventory given as a parameter"""
        for item in self.drop:
            player_inv.add_inv(item)


class shop():
    """class shop to hold a list of items that the merchant can carry"""
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
        """Built in function to make the object subscriptable"""
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
        """Function to return a list of string about the item details"""
        L=[]
        c = 1
        for i in self.Shop:
            L.append(f"{c}. {i.name} : {i.desc}")
            c+=1
        return L


