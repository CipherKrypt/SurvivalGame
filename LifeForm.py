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
        self.hydration = (self.hp)%10
        self.energy = (self.hp)%10
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
            fun= function('Drink',1,5)
        elif function_name == 'eat':
            fun= function('Eat',2,5)
        elif function_name == 'equip':
            fun= function('Equip',3,0)
        elif function_name == 'scout':
            fun = function('Scout',4,0)
        elif function_name == 'inventory':
            fun == function('Check Inventory',5,0)
        elif function_name == 'scratch':
            fun = function('Scratched',0,20)
        elif function_name == 'bite':
            fun = function('Bit',0,30)
        elif function_name == 'heal':
            fun = function('Eat',6,20)
        elif function_name == 'evade':
            escape=52-2*self.xp.lvl
            if escape <0:
                escape=0
            fun = function('Evaded',8,escape)
        elif function_name == 'attack':
            fun = function('Attack',0,20)
        elif function_name == 'chop':
            fun = function('Chop',0,1)
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
            Item = item('Axe',1,'An item that can be equipped to cut down trees',moves(self.premade_function('equip'),
                                                                                       self.premade_function('chop'),
                                                                                       self.premade_function('attack').set_var(10+10*self.xp.lvl)))
        elif item_name == 'berry':
            Item = item('Berry',1,'A Consumable that will replenish HP',moves(self.premade_function('heal')))
        elif item_name == 'gold':
            Item = item('Gold',1,'Gold can be found or dropped by wolves. Use it to buy items from merchants',None)
        elif item_name == 'torch':
            Item = item('Torch',1,'An item that consumes 1xwood per cycle to provide fire and ward off Wolves when equiped',moves(self.premade_function('fire')))
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
            pass
        elif func.function_code == 2:# Eat
            pass
        elif func.function_code == 3:# Equip
            pass
        elif func.function_code == 4:
            if 'Light' in self.equip.att.list_it():
                if self.inventory.use_item('Wood'):
                    self.location.decrease_attribute('w',self.equip.att[0].var)
            scouted=self.location.search()
            if scouted[8]:#Attack by Wolf
                if self.equip.name != 'torch':
                    wolf=self.premade_animal('wolf')
                    try:
                        print('\n'
                              'Yikes! You encountered a wolf. You heard it gives some useful drops but maybe escaping is wiser')
                        run=True
                        while not wolf.is_dead():
                            print('Do you want to...')
                            print('Attack   Inventory   Nothing',end='')
                            if run:
                                print('Run')
                            print(self.__str__())
                            ch=input('Enter>> ')
                            ch=ch.lower().lstrip().rstrip()
                            if ch == 'help' or ch == '!h':
                                raise NeedHelp
                            elif ch == 'attack' or ch == 'nothing':
                                if ch == 'attack' and 'attack' in self.equip.att.list_it():
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
                try:
                    while not tree.is_cut:
                        print('Do you want to....')
                        print('Chop    Inventory   Pass')
                        ch=input('Enter>> ')
                        ch = ch.lower().lstrip().rstrip()
                        if ch == 'help' or ch == '!h':
                            raise NeedHelp
                        if ch == 'chop':
                            if 'chop' in self.equip.att.list_it():
                                tree.is_cut=True
                                wood=tree.wood*self.equip.att["chop"]
                                print(f'Nice! You collected {str(wood)}xWood.\n')
                                self.inventory.add_inv(self.premade_item('wood').set_amnt(wood))
                            else:
                                print('You need to equip something that can chop,to chop the tree\n')
                                continue
                        elif ch == 'inventory':
                            self.enact(self.actions[1])
                        elif ch == 'pass':
                            print('Meh...Extra wood is just extra baggage...You can probably make do with what you got')
                            break
                        else:
                            raise WrongEntry

                except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == DeathByDamage:
                            return Err
            if scouted[3]:#Found Berry
                print("Hey Look! A berry! Should you take it... might be poisonous.")
                while True:
                    try:
                        print('Do you want to...\n'
                              'Collect   Pass')
                        ch = input('Enter>> ')
                        ch = ch.lower().lstrip().rstrip()
                        if ch == 'help' or ch == '!h':
                            raise NeedHelp
                        elif ch == 'collect':
                            self.collect(self.premade_item('berry'))
                            break
                        elif ch == 'pass':
                            print("You don't touch it. Could be deadly. You will never know.")
                            break
                        else:
                            raise WrongEntry
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
                        print('Do you want to...\n'
                              'Refill   Pass')
                        print(self.__str__())
                        ch=input('Enter>> ')
                        ch=ch.lower().rstrip().lstrip()
                        if ch == 'help' or ch == '!h':
                            raise NeedHelp
                        elif ch == 'refill':
                            self.hydration=self.hp%10
                            self.inventory.add_inv(self.premade_function('water').set_var(5))
                            break
                        elif ch == 'pass':
                            print('Na..Too lazy, besides your not thirsty... Yet.')
                            break
                        else:
                            raise WrongEntry
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again!')
                        else:
                            pass

            if scouted[5]:#Found a hen
                hen=self.premade_animal('hen')
                print('You came across a hen. Chicken for dinner sounds good ...Yum!')
                while True:
                    try:
                        print('Do you want to...\n'
                              'Hunt   Inventory   Pass')
                        print(self.__str__())
                        ch=input('Enter>> ')
                        ch=ch.lower().lstrip().rstrip()
                        if ch == 'help' or ch == '!h':
                            raise NeedHelp
                        elif ch == 'hunt':
                            if not self.enact(hen.move[0]):
                                print(f'Here...buck.buck.buck.. -catches hen- Nice! got {hen.drops.content()}!')
                                self.collect(hen.drops.collect(self.inventory))
                            else:
                                print("Sheesh! It got away... Maybe next time.")
                            break
                        elif ch == 'inventory':
                            self.enact(self.premade_function('inventory'))
                        elif ch == 'pass':
                            print("That hen seems to be in a 'fowl' mood -pun- it might peck. Surely the next one.")
                            break
                        else:
                            raise WrongEntry
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try again!')
                        else:
                            pass
            if scouted[6]:  # Found a pig
                pig = self.premade_animal('pig')
                print('You came across a pig. Hmmm....you can already smell the bacon...Yum!')
                while True:
                    try:
                        print('Do you want to...\n'
                              'Hunt   Inventory   Pass')
                        print(self.__str__())
                        ch = input('Enter>> ')
                        ch = ch.lower().lstrip().rstrip()
                        if ch == 'help' or ch == '!h':
                            raise NeedHelp
                        elif ch == 'hunt':
                            if not self.enact(pig.move[0]):
                                print(f'If you move reeeaaalll slow, you might become invisible -catches pig- Cool! got {pig.drops.content()}!')
                                self.collect(pig.drops.collect(self.inventory))
                            else:
                                print("Man! That pig was FAST!... So much for your bacon -eyeroll-.")
                            break
                        elif ch == 'inventory':
                            self.enact(self.premade_function('inventory'))
                        elif ch == 'pass':
                            print("Oh you just realised....you don't know how to cook bacon. -shrug-")
                            pass
                        else:
                            raise WrongEntry
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again!')
                        else:
                            pass

            if scouted[7]: #found Gold
                print("Huh? What is that shining? Oh, looks like Gold!")
                while True:
                    try:
                        print('Do you want to...\n'
                              'Collect   Pass')
                        ch=input('Enter>> ')
                        ch=ch.lower().lstrip().rstrip()
                        if ch == 'help' or ch=='!h':
                            raise NeedHelp
                        elif ch == 'collect':
                            self.collect(self.premade_item('gold'))
                            break
                        elif ch == 'pass':
                            print("Nah....looks like Fool's Gold...you walk away from the gold. A Fool!")
                            break
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again')
            return
        elif func.function_code == 5:# Check Inventory





    def collect(self,items:item):
        print(f'You found a {str(items.amnt)}{items.name}: {items.desc}')
        while True:
            try:
                print('Do you want to collect or pass?')
                ch=input('Enter>> ')
                ch = ch.lower().rstrip().lstrip()
                if ch == 'help' or ch == '!h':
                    raise NeedHelp
                elif ch == 'collect':
                    print(f'You collected {str(items.amnt)}x{items.name}')
                    print()
                    self.inventory.add_inv(items)
                elif ch == 'pass':
                    break
                else:
                    raise WrongEntry

            except Exception as Err:
                if Err == WrongEntry
                    print('Wrong Entry! Try again!')
                elif Err == NeedHelp:
                    self.help()
                else:
                    pass

