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
        else:
            self.hp -=damage
        return self.is_dead()

class Exp():
    def __init__(self,xp=0,next_lvl=50,lvl=1):
        self.xp=xp
        self.next_lvl=next_lvl
        self.lvl=lvl

    def __str__(self):
        return f'Level: {str(self.lvl)} XP: {str(self.xp)} Next Level in: {str(self.next_lvl-self.xp)}'

    def check_xp(self,lvl_up:False):
        if self.xp==self.next_lvl:
            self.xp=0
            self.lvl+=1
            self.next_lvl*=2
        elif self.xp>self.next_lvl:
            self.xp-=self.next_lvl
            self.lvl+=1
            self.next_lvl*=2
        if self.xp<self.next_lvl:
            if lvl_up:
                print('Woah! You Leveled Up...')
                print(self.xp)
            return
        else:
            self.check_xp(True)

    def add_xp(self,xp:int):
        self.xp+=xp
        self.check_xp()
        print(f'You got {xp} XP!')



class Animal(Life):
    def __init__(self,max_hp:int,animal:str,desc:str,drops:drop,move:moves):
        super().__init__(max_hp)
        self.animal=animal
        self.desc=desc
        self.drops=drops
        self.move=move

    def __str__(self):
        return super().__str__()+f' called {self.animal}.\n' \
                                 f'Description: {self.desc}\n' \
                                 f'Contains drops....\n' \
                                 f'{self.drops}'

class Tree(Life):
    def __init__(self,wood:int):
        self.wood=wood
        self.is_cut=False

    def __str__(self):
        return f'a Tree object that will drop {self.wood} wood'

    def cut(self):
        pass


class Player(Life):
    def __init__(self,max_hp):
        super().__init__(max_hp)
        self.xp=Exp()
        self.inventory=self.premade_inventory()
        self.location:Location=self.premade_location('wild')
        self.turn = 0
        self.equip:item or None = None
        self.hydration = (self.hp)/10
        self.energy = (self.hp)/10
        self.subject:Animal or item or Tree or None = None
        self.actions=moves(self.premade_function('scout'),self.premade_function('inventory'))

    def __str__(self):
        if self.equip == None:
            equiped='Nothing'
        else:
            equiped=self.equip.name
        return f'Your Hp: {str(self.hp)}/{str(self.max_hp)} Hydration: {str(self.hydration)} Energy: {str(self.energy)} Equiped: {equiped}'

    def cycle(self):
        print()
        if self.turn==10:
            self.turn=1
            self.location.decrease_attribute('w', 30)
        else:
            self.turn+=1
        if self.turn >=5:
            self.location.increase_attribute('w',30)
        self.hydration-=2*self.location.thirst_mult
        if self.hydration<=20:
            print(f'(!) Your Hydaration is {str(self.hydration)}. You need Water stat! Keep it above 20 else you lose energy!')
            self.energy-=5
        if self.hydration<=0:
            raise DeathByDehydration
        self.energy-=5
        if self.energy>=50:
            self.regenerate(5*self.xp.lvl)
        if self.energy<=30:
            print(f'(!) Your Energy is {str(self.energy)}. You need Food stat! Keep it above 30 else you lose Hp!')
            if self.hit(5):
                raise DeathByStarvation
        if self.energy<=0:
            raise DeathByStarvation
        if self.hp <=100:
            print(f'(!)Your Hp is at a Critical Level. Only {str(self.hp)} HP left. Be careful! Try to Heal!')

    def get_ch(self):
        print('Do you want to...')
        print(self.actions.print_it())
        print(self.__str__())
        ch = input('Enter>> ')
        ch = ch.lower().rstrip().lstrip()
        if ch == 'help' or ch.lower() == '!h':
            raise NeedHelp
        elif ch in self.actions.list_it():
            func = self.actions[ch]
            self.enact(func)
        else:
            raise WrongEntry

    def game_over(self,Err:Exception=None):
        if Err == DeathByDamage:
            print("\n"
                  "You couldn't handle that Damage.... \n"
                  "As you lose your consciousness.... "
                  "You can't believe that the last thing you feel is excruciating pain.\n"
                  "You died.")
        elif Err == DeathByDehydration:
            print("\n"
                  "Your throat feels like paper....so dry...so tired....\n"
                  "You feel sleepy...maybe a few minutes of sleep is what you need....you close your eyes\n"
                  "Minutes passed....Hours passed...but your eyes will never open again.\n"
                  "You died.")
        elif Err == DeathByStarvation:
            print("\n"
                  "Your feeling cold and weak and you can't think straight...\n"
                  "You tell your self,'I wish I had never.......'\n"
                  "but you would never complete that thought...your heart stopped.\n"
                  "You died")

    def help(self):
        print('Help')

    def equip_item(self,Item:item):
        self.equip=Item

    def premade_location(self,location_name:str)->Location:
        if location_name == 'wild':
            location = Location('Wilderness', 1.5, 0, 10, 50, 50, 10, 30, 40, 20, 10, 20)
        else:
            raise NotAnAttribute
        return location

    def premade_function(self,function_name:str)-> function:
        if function_name == 'drink':
            fun = function('Drink',1,5)
        elif function_name == 'eat':
            fun = function('Eat',2,5)
        elif function_name == 'equip':
            fun = function('Equip',3,0)
        elif function_name == 'scout':
            fun = function('Scout',4,0)
        elif function_name == 'inventory':
            fun = function('Check Inventory',5,0)
        elif function_name == 'hunt':
            fun = function('Hunt',6,0)
        elif function_name == 'refill':
            fun = function('Refill',7,0)
        elif function_name == 'pass':
            fun = function('Pass',8,0)
        elif function_name == 'collect':
            fun = function('Collect',9,0)
        elif function_name == 'chop':
            fun = function('Chop',10,0)
        elif function_name == 'scratch':
            fun = function('Scratched',0,20)
        elif function_name == 'bite':
            fun = function('Bit',0,30)
        elif function_name == 'heal':
            fun = function('Eat',11,20)
        elif function_name == 'evade':
            escape=52-2*self.xp.lvl
            if escape <0:
                escape=0
            fun = function('Evaded',12,escape)
        elif function_name == 'return':
            fun = function('Return',13,0)
        elif function_name == 'damage':
            fun = function('Damage',0,20)
        elif function_name == 'chopper':
            fun = function('Chopper',0,1)
        elif function_name == 'light':
            fun = function('Light',0,20)
        elif function_name == 'fire':
            fun = function('Fire',0,1)
        else:
            raise NotAnAttribute
        return fun

    def premade_item(self,item_name:str)-> item:
        if item_name == 'water':
            Item = item('Water',5,'A Consumable that will replenish Hydration',moves(self.premade_function('drink')))
        elif item_name == 'wood':
            Item = item('Wood',1,'Consumable dropped by Trees',None)
        elif item_name == 'chicken':
            Item = item('Meat',1,'Consumable dropped by Hen and Pig that will replenish Energy',moves(self.premade_function('eat')))
        elif item_name == 'pork':
            Item = item('Meat', 2, 'Consumable dropped by Hen and Pig that will replenish Energy',moves(self.premade_function('eat')))
        elif item_name == 'axe':
            Item = item('Axe',1,'An item that can be equipped to cut down trees',moves(self.premade_function('equip'),self.premade_function('chopper'),self.premade_function('damage')))
        elif item_name == 'berry':
            Item = item('Berry',1,'A Consumable that will replenish HP',moves(self.premade_function('heal')))
        elif item_name == 'gold':
            Item = item('Gold',1,'Gold can be found or dropped by wolves. Use it to buy items from merchants',None)
        elif item_name == 'torch':
            Item = item('Torch',1,'An item that consumes 1xwood per cycle to provide fire and ward off Wolves when equiped',moves(self.premade_function('equip'),self.premade_function('light'),self.premade_function('fire')))
        else:
            raise NotAnAttribute
        return Item

    def premade_inventory(self)-> inventory:
        invent = inventory(self.premade_item('water'), self.premade_item('axe'))
        return invent

    def premade_animal(self,animal_name:str) -> Animal:
        if animal_name == 'wolf':
            animal = Animal(100*self.xp.lvl,'Wolf',
            'Beware the wolf that roam the Wild.\nEspecially at night. Equip a torch at night to ward of wolves lest they attack you.',
                          drop(self.premade_item('gold').set_amnt(1*self.xp.lvl)),moves(self.premade_function('scratch'),self.premade_function('bite')))
        elif animal_name == 'hen':
            animal = Animal(1,'Hen','Animal that can drop Meat that can be consumed to raise Energy',
                            drop(self.premade_item('chicken').set_amnt(1*self.xp.lvl)),moves(self.premade_function('evade')))
        elif animal_name == 'pig':
            animal = Animal(1,'Pig','Animal that can drop Meat that can be consumed to raise Energy',
                            drop(self.premade_item('pork').add_item(1*self.xp.lvl)),moves(self.premade_function('evade')))
        return animal


    def enact(self,func:function):
        if func.function_code == 1:# Drink
            self.hydration+=func.var
            print('Ah! That was a refreshing drink')
        elif func.function_code == 2:# Eat
            self.energy+=func.var
            print('Maaaaan! That was good!')
        elif func.function_code == 3:# Equip
            self.equip_item(self.subject)
            print(f'You equipped {self.subject.name}')
        elif func.function_code == 4:
            if self.equip != None:
                if 'Light' in self.equip.att.list_it():
                    if self.inventory.use_item('Wood'):
                        self.location.decrease_attribute('w',self.equip.att[0].var)
            scouted=self.location.search()
            print('scouted')

            if scouted[8]:#Attack by Wolf
                while True:
                    if self.equip == None:
                        break
                    if 'damage' in self.equip.att.list_it():
                        break
                    else:
                        return

                wolf=self.premade_animal('wolf')
                try:
                    print('\n'
                          'Yikes! You encountered a wolf. You heard it gives some useful drops but maybe escaping is wiser')
                    run=True
                    while not wolf.is_dead():
                        print('Do you want to...')
                        print('attack   inventory   nothing   ',end='')
                        if run:
                            print('run')
                        else:
                            print()
                        print(self.__str__())
                        ch=input('Enter>> ')
                        ch=ch.lower().lstrip().rstrip()
                        if ch == 'help' or ch == '!h':
                            raise NeedHelp
                        elif ch == 'attack' or ch == 'nothing':
                            if self.equip == None:
                                print('You need to equip something that can deal damage\n')
                                continue
                            elif ch == 'attack' and 'damage' in self.equip.att.list_it():
                                print(f'You dealed {str(self.equip.att[1].var)} Damage.')
                                if wolf.hit(self.equip.att[1].var):
                                    print(f'Phew! The wolf ran way....Woah it dropped {wolf.drops.content()}!')
                                    self.collect(wolf.drops.collect(self.inventory))
                                    self.xp.add_xp(wolf.max_hp%10)
                                    break
                            else:
                                print('You need to equip something that can deal damage\n')
                                continue
                            from random import choice
                            m:function=choice(list(wolf.move))
                            print(f'The wolf {m.name} you and dealed {str(m.var)} damage!')
                            if self.hit(m.var):
                                raise DeathByDamage
                            else:
                                continue
                        elif ch == 'run' and run:
                            from random import randint
                            if randint(1,100)<=(5+5*self.xp.lvl):
                                print('\n'
                                      "Phew! It seemed the wolf wasn't interested in you. You escaped")
                                break
                            else:
                                print('\n'
                                      'Oh No! The wolf caught your scent! You have to fight')
                                run=False
                                continue
                        elif ch == 'inventory':
                            self.enact(self.actions[1])
                        else:
                            raise WrongEntry
                except Exception as Err:
                    if Err == NeedHelp:
                        self.help()
                    elif Err == DeathByDamage:
                        return Err
                    elif Err == WrongEntry:
                        print('Invalid Entry...Try again')
                    else:
                        pass

            if scouted[2]:#Found a Tree
                from random import randint
                lv=self.xp.lvl
                wood=randint(1*lv,2+1*lv)
                tree=Tree(wood)
                print('You found a tree. Chop Chop')
                self.subject = tree
                try:
                    while not tree.is_cut:
                        self.actions = moves(self.premade_function('chop'),self.premade_function('inventory'),self.premade_function('pass'))
                        self.get_ch()
                except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == DeathByDamage:
                            return Err
            if scouted[3]:#Found Berry
                print("Hey Look! A berry! Should you take it... might be poisonous.")
                self.subject = self.premade_item('berry')
                while True:
                    try:
                        self.actions= moves(self.premade_function('collect'),self.premade_function('pass'))
                        self.get_ch()
                        break
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again!')
                        else:
                            pass
            if scouted[4]:#Found a water source
                print('You found a water source. Maybe you should refill your Canteen')
                while True:
                    try:
                        self.actions = moves(self.premade_function('refill'),self.premade_function('pass'))
                        break
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again!')
                        else:
                            pass

            if scouted[5]:#Found a hen
                self.subject=self.premade_animal('hen')
                print('You came across a hen. Chicken for dinner sounds good ...Yum!')
                while True:
                    try:
                        self.actions=moves(self.premade_function('hunt'),self.premade_function('inventory'),self.premade_function('pass'))
                        if self.get_ch():
                            break
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try again!')
                        else:
                            pass
            if scouted[6]:  # Found a pig
                self.subject = self.premade_animal('pig')
                print('You came across a pig. Hmmm....you can already smell the bacon...Yum!')
                while True:
                    try:
                        self.actions = moves(self.premade_function('hunt'), self.premade_function('inventory'),self.premade_function('pass'))
                        self.get_ch()
                        break
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again!')
                        else:
                            pass

            if scouted[7]: #found Gold
                print("Huh? What is that shining? Oh, looks like Gold!")
                self.subject = self.premade_item('gold')
                while True:
                    try:
                        self.actions = moves(self.premade_function('collect'),self.premade_function('pass'))
                        self.get_ch()
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again')
            return
        elif func.function_code == 5:# Check Inventory
            print("\n"
                  "Your Inventory\n"
                  "---------------")
            if self.inventory == None:
                print('-Nothing in Inventory-')
                return
            inv=self.inventory.list_inv()
            for i in range(len(inv)):
                print(f'{str(i+1)}. {inv[i].name}')
            try:
                ch = int(input('Enter item number>> '))
                if ch <= len(inv)+1:
                    print('y')
                    items:item=self.inventory[ch-1]
                    self.subject = items
                    print(items)
                    self.actions = moves(items.att[0], self.premade_function('return'))
                    self.get_ch()
            except Exception as Err:
                if Err == NeedHelp:
                    self.help()
                elif Err == WrongEntry:
                    print('Wrong Entry! Try Again!')
                else:
                    pass
        elif func.function_code == 6: # Hunt the Animal
            print('Hunt')
            animal = self.subject
            if animal.animal == 'Hen':
                    if not self.enact(animal.move[0]):
                        print(f'Here...buck.buck.buck.. -catches hen- Nice! got {animal.drops.content()}!')
                        self.collect(animal.drops.collect(self.inventory))
                        return True
                    else:
                        print("Sheesh! It got away... Maybe next time.")
                        return True
            if animal.animal == 'Pig':
                if not self.enact(animal.move[0]):
                    print(f'If you move reeeaaalll slow, you might become invisible -catches pig- Cool! got {animal.drops.content()}!')
                    self.collect(animal.drops.collect(self.inventory))
                    return True
                else:
                    print("Man! That pig was FAST!... So much for your bacon -eyeroll-.")
                    return True

        elif func.function_code == 7:# Refill
            print('Refill')
            self.hydration = self.hp / 10
            self.inventory.add_inv(self.premade_function('water').set_var(5))

        elif func.function_code == 8:# Pass
            print('Pass')
            if type(self.subject) == Animal:
                animal = self.subject
                if animal.animal == 'Hen':
                    print("That hen seems to be in a 'fowl' mood -pun-. It might peck. You're not that 'peckish' -another pun-.")
                if animal.animal == 'Pig':
                    print("Oh you just realised....you don't know how to cook bacon. -shrug-")
            if type(self.subject) == item:
                items:item= self.subject
                if items.name == 'Berry':
                    print("You don't touch it. Could be deadly. You will never know.")
                if items.name == 'Gold':
                    print("Nah....looks like Fool's Gold...you walk away from the gold. A Fool!")
            if type(self.subject) == Tree:
                print('Meh...Extra wood is just extra baggage...You can probably make do with what you got')
            if type(self.subject) == None:
                print('Na..Too lazy, besides your not thirsty... Yet.')

            print()

        elif func.function_code == 9:# Collect
            print('Collect')
            items = self.subject
            self.collect(items)

        elif func.function_code == 10:# Chop
            print('Chop')
            tree= self.subject
            try:
                if self.equip == None:
                    print('You need to equip something that has chopper attribute,to chop the tree\n')
                    return
                elif 'chopper' in self.equip.att.list_it():
                    tree.is_cut = True
                    wood = tree.wood * self.equip.att["chop"].var
                    print(f'Nice! You collected {str(wood)}xWood.\n')
                    self.inventory.add_inv(self.premade_item('wood').set_amnt(wood))
                else:
                    print('You need to equip something that has chopper attribute,to chop the tree\n')
                    return
            except Exception as e:
                print(e)

        elif func.function_code == 11:# Heal
            print('Heal')
            self.regenerate(50)
            self.inventory.use_item(self.subject)

        elif func.function_code == 12:# Evade
            print('Evade')
            from random import randint
            if randint(0,100)<=func.var:
                print('True')
                return True
            else:
                print('False')
                return False

        elif func.function_code == 13:# Return
            return

    def collect(self,items:item):
        print(f'You found a {str(items.amnt)}{items.name}: {items.desc}')
        print(f'You collected {str(items.amnt)}x{items.name}')
        print()
        self.inventory.add_inv(items)


