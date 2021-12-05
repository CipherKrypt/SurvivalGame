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
        self.day = 1
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
            self.day+=1
            self.turn=1
            self.location.decrease_attribute('w', 30)
        else:
            self.turn+=1
        if self.turn >=5:
            self.location.increase_attribute('w',30)
        if self.day == 30:
            self.game_over(Survived)
            return
        self.hydration-=2*self.location.thirst_mult
        if self.hydration<=0:
            self.game_over(DeathByDehydration)
            return
        if self.hydration<=20:
            print(f'(!) Your Hydaration is {str(self.hydration)}. You need Water stat! Keep it above 20 else you lose energy!')
            self.energy-=5
        self.energy-=5
        if self.energy>=50:
            self.regenerate(5*self.xp.lvl)
        if self.energy<=30:
            print(f'(!) Your Energy is {str(self.energy)}. You need Food stat! Keep it above 30 else you lose Hp!')
            if self.hit(5):
                self.game_over(DeathByStarvation)
                return
        if self.energy<=0:
            self.game_over(DeathByStarvation)
            return
        if self.hp <=100:
            print(f'(!)Your Hp is at a Critical Level. Only {str(self.hp)} HP left. Be careful! Try to Heal!')

    def get_ch(self):
        print('Do you want to...')
        print(self.actions.print_it())
        print(self.__str__())
        ch = input('Enter>> ')
        ch = ch.lower().rstrip().lstrip()
        if ch == 'help' or ch == '!h':
            self.help()
            return False
        elif ch in self.actions.list_it():
            func = self.actions[ch]
            return self.enact(func)
        else:
            return WrongEntry

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
        elif Err == Survived:
            print("\n"
                  "Oh no... is that Thunder!? It's going to rain!?...\n"
                  "Wait...it isn't thunder... it's....'\n"
                  "A Helicopter!!! It's landing by the beach! You run towards the Helicopter\n"
                  "Your saved!"
                  "Or are you.....")
        self.hp=0

    def help(self):
        print('Help Menu:')
        print(f'''
        Your task in this game is to survive the open world for 30 days
        so that help can arrive...
        Each day is composed of 10 cycles. 5 cycles for Morning and 5 for Night.
        Beware of the Night! You are more likely to encounter wolves. Equip items that can ward them off.
        Your standing so far:
        {self.__str__()}
        Keep an eye on your Health, Hydration and Energy
        if your Hydration goes below 20, you start losing Energy
        if your Energy goes below 30, you start losing HP
        and if your HP becomes 0.....well congratulations! Now you know how NOT to play this game.
        
        How to Play:
        Everytime you can make a choice...
        your options will be show under 'Do you want to...'
        'Type In' the option name to proceed EXCEPT when choosing items in inventory...
        at that time enter the number assigned to the item.
        
        Your Inventory:
        Everytime you choose 'check inventory' you will be shown your Inventory.
        When you select an item...everything about it will be displayed
        Keep an out for Attributes...they govern what you can do with items that you equip...
        like whether you can deal damage or chop down trees etc.
        
        Well...That's all the help I can offer you..
        Your journey ahead, is your own... What awaits you?
        Only time can tell......
        ''')

    def equip_item(self,Item:item):
        self.equip=Item

    def premade_location(self,location_name:str)->Location:
        if location_name == 'wild':
            location = Location('Wilderness', 1.5, 0, 10, 50, 50, 10, 30, 40, 20, 10, 20)
        else:
            return NotAnAttribute
        return location

    def premade_function(self,function_name:str)-> function:
        if function_name == 'drink':
            fun = function('drink',1,5)
        elif function_name == 'eat':
            fun = function('eat',2,5)
        elif function_name == 'equip':
            fun = function('equip',3,0)
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
            return NotAnAttribute
        return fun

    def premade_item(self,item_name:str)-> item:
        if item_name == 'water':
            Item = item('Water',5,'A Consumable that will replenish Hydration by 5 points',moves(self.premade_function('drink')))
        elif item_name == 'wood':
            Item = item('Wood',1,'Consumable dropped by Trees',None)
        elif item_name == 'chicken':
            Item = item('Meat',1,'Consumable dropped by Hen and Pig that will replenish Energy by 5 points',moves(self.premade_function('eat')))
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
            return NotAnAttribute
        return Item

    def premade_inventory(self)-> inventory:
        invent = inventory(self.premade_item('axe'))
        return invent

    def premade_animal(self,animal_name:str) -> Animal:
        if animal_name == 'wolf':
            gold=self.premade_item('gold')
            gold.set_amnt(1*self.xp.lvl)
            animal = Animal(100*self.xp.lvl,'Wolf',
            'Beware the wolf that roam the Wild.\nEspecially at night. Equip a torch at night to ward of wolves lest they attack you.',

                          drop(gold),moves(self.premade_function('scratch'),self.premade_function('bite')))
        elif animal_name == 'hen':
            chicken=self.premade_item('chicken')
            chicken.set_amnt(1 * self.xp.lvl)
            animal = Animal(1,'Hen','Animal that can drop Meat that can be consumed to increase Energy',
                            drop(chicken),moves(self.premade_function('evade')))
        elif animal_name == 'pig':
            pork=self.premade_item('pork')
            pork.add_item(1*self.xp.lvl)
            animal = Animal(1,'Pig','Animal that can drop Meat that can be consumed to increase Energy',
                            drop(pork),moves(self.premade_function('evade')))
        return animal


    def enact(self,func:function):
        if func.function_code == 1:#
            cond = self.inventory.use_item('water')
            if cond:
                max_val=self.max_hp/10
                max_val = float(max_val)
                if self.hydration == max_val:
                    print("You weren't thirsty, but who doesn't like a good drink")

                else:
                    print('Ah! That was a refreshing drink')
                    if float(self.hydration + func.var) >= max_val:
                        self.hydration = max_val
                        print('You are now fully hydrated')
                    else:
                        self.hydration+=float(func.var)
                        print(f'Hydration + {func.var}')
                print()
                return False
        elif func.function_code == 2:# Eat
            cond = self.inventory.use_item('meat')
            if cond:
                max_val = self.max_hp / 10
                max_val = float(max_val)
                if self.inventory.use_item('meat'):
                    if self.energy == float(max_val):
                        print("You weren't hungry, but today is cheat day")

                    else:
                        print('Maaaan!That was good!')
                        if float(self.energy + func.var) >= float(max_val):
                            self.energy = max_val
                            print('You have full Energy')
                        else:
                            self.energy += func.var
                            print(f'Energy + {func.var}')
                print()
                return False
        elif func.function_code == 3:# Equip
            self.equip_item(self.subject)
            print(f'You equipped {self.subject.name}\n')
        elif func.function_code == 4:# Scout
            if self.equip != None:
                if 'Light' in self.equip.att.list_it():
                    if self.inventory.use_item('Wood'):
                        self.location.decrease_attribute('w',self.equip.att[0].var)
            scouted=self.location.search()
            print('You start to scout the area...\n')
            found = False
            if scouted[8]:#Attack by Wolf
                found = True
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
                        print('attack   check inventory   nothing   ',end='')
                        if run:
                            print('run')
                        else:
                            print()
                        print(f"Wolf's HP: {str(wolf.hp)}")
                        print(self.__str__())
                        ch=input('Enter>> ')
                        ch=ch.lower().lstrip().rstrip()
                        if ch == 'help' or ch == '!h':
                            return NeedHelp
                        elif ch == 'attack' or ch == 'nothing':
                            if ch=='attack':
                                if self.equip == None:
                                    print('You need to equip something that can deal damage\n')
                                    continue
                                elif ch == 'attack' and 'damage' in self.equip.att.list_it():
                                    print(f'You dealed {str(30*self.equip.att[1].var)} Damage.\n')
                                    if wolf.hit(30*self.equip.att[1].var):
                                        print(f'Phew! The wolf ran way....Woah it dropped {wolf.drops.content()} !')
                                        self.collect(wolf.drops.collect(self.inventory))
                                        self.xp.add_xp(wolf.max_hp%10)
                                        break
                                else:
                                    print('You need to equip something that can deal damage\n')
                                    continue
                            from random import choice
                            m:function=choice(list(wolf.move))
                            print(f'The wolf {m.name} you and dealed {str(m.var)} damage!\n')
                            if self.hit(m.var):
                                self.game_over(DeathByDamage)
                                return
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
                        elif ch == 'check inventory':
                            self.enact(self.premade_function('inventory'))
                            continue
                        else:
                            return WrongEntry
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
                found = True
                try:
                    while True:
                        from random import randint
                        lv = self.xp.lvl
                        wood = randint(1 * lv, 2 + 1 * lv)
                        print('You found a tree. Chop Chop')
                        Wood = self.premade_item('wood')
                        Wood.set_amnt(wood)
                        self.subject = Wood
                        self.actions = moves(self.premade_function('chop'),self.premade_function('inventory'),self.premade_function('pass'))
                        cond=self.get_ch()
                        if cond:
                            break
                except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == DeathByDamage:
                            return Err
            if scouted[3]:#Found Berry
                found = True
                print("Hey Look! A berry! Should you take it?.. might be poisonous.")
                while True:
                    try:
                        self.subject = self.premade_item('berry')
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
                    break
            if scouted[4]:#Found a water source
                found = True
                print('You found a water source. Maybe you should refill your Canteen')

                while True:
                    try:
                        self.subject = None
                        self.actions = moves(self.premade_function('refill'),self.premade_function('pass'))
                        self.get_ch()
                        break
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again!')
                        else:
                            print (Err)
                    break

            if scouted[5]:#Found a hen
                found = True
                print('You came across a hen. Chicken for dinner sounds good ...Yum!')
                while True:
                    try:
                        self.subject = self.premade_animal('hen')
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
                    break

            if scouted[6]:  # Found a pig
                found = True
                print('You came across a pig. Hmmm....you can already smell the bacon...Yum!')
                while True:
                    try:
                        self.subject = self.premade_animal('pig')
                        self.actions = moves(self.premade_function('hunt'), self.premade_function('inventory'),self.premade_function('pass'))
                        if self.get_ch():
                            break

                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again!')
                        else:
                            pass
                    break

            if scouted[7]: #found Gold
                found = True
                print("Huh? What is that shining? Oh, looks like Gold!")
                while True:
                    try:
                        self.subject = self.premade_item('gold')
                        self.actions = moves(self.premade_function('collect'),self.premade_function('pass'))
                        self.get_ch()
                        break
                    except Exception as Err:
                        if Err == NeedHelp:
                            self.help()
                        elif Err == WrongEntry:
                            print('Wrong Entry! Try Again')
                    break
            if found:
                print("Phew! All in a days work...Now what to do?")
            else:
                print("Maaan! All that walking and you didn't find ANYTHING!? Try again")
            try:
                ch = input(Enter>>'')
            return True
        elif func.function_code == 5:# Check Inventory
            print("\n"
                  "Your Inventory\n"
                  "---------------")
            if self.inventory == None:
                print('-Nothing in Inventory-')
                return False
            inv=self.inventory.list_inv()
            print('0. Exit')
            for i in range(len(inv)):
                print(f'{str(i+1)}. {inv[i].name}')
            try:
                ch = int(input('Enter item number>> '))
                if ch <= len(inv)+1:
                    items:item=self.inventory[ch-1]
                    self.subject = items
                    print(items)
                    try:
                        self.actions = moves(items.att[0], self.premade_function('return'))
                    except:
                        self.actions = moves(self.premade_function('return'))
                    self.get_ch()
                elif ch == 0:
                    return False
            except Exception as Err:
                if Err == NeedHelp:
                    self.help()
                elif Err == WrongEntry:
                    print('Wrong Entry! Try Again!')
                else:
                    pass
            return False
        elif func.function_code == 6: # Hunt the Animal
            animal = self.subject
            if animal.animal == 'Hen':
                    if self.enact(animal.move[0]):
                        print("Sheesh! It got away... Maybe next time.")
                        return True
                    else:
                        print(f'Here...buck.buck.buck.. -catches hen- Nice! got {animal.drops.content()}!')
                        self.collect(animal.drops.collect(self.inventory))
                        return True

            if animal.animal == 'Pig':
                if self.enact(animal.move[0]):
                    print("Man! That pig was FAST!... So much for your bacon -eyeroll-.")
                    return True
                else:
                    print(f'If you move reeeaaalll slow, you might become invisible -catches pig- Cool! got {animal.drops.content()}!')
                    self.collect(animal.drops.collect(self.inventory))
                    return True


        elif func.function_code == 7:# Refill
            print('Ah....That was a good drink. You fill your canteen\n')
            self.hydration = self.max_hp / 10
            water = self.premade_item('water')
            water.set_amnt(5)
            self.inventory.add_inv(water)
            print(f'{str(water.amnt)}xWater added to Inventory\n')

        elif func.function_code == 8:# Pass
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
                if item.name == 'Wood':
                    print('Meh...Extra wood is just extra baggage...You can probably make do with what you got')
            else:
                print('Na..Too lazy, besides your not thirsty... Yet.')
            print()
            return True


        elif func.function_code == 9:# Collect
            items = self.subject
            self.collect(items)

        elif func.function_code == 10:# Chop
            try:
                wood = self.subject
                if self.equip == None:
                    print('You need to equip something that has chopper attribute,to chop the tree\n')
                    return False
                elif 'chopper' in self.equip.att.list_it():
                    m = self.equip.att["chopper"].var
                    print('Heave Ho! annnndddd.... Lumber!\n')
                    wood.set_amnt(wood.amnt * m)
                    print(f'Nice! You collected {str(wood.amnt)}xWood.\n')
                    self.inventory.add_inv(wood)
                    return True
                else:
                    print('You need to equip something that has chopper attribute,to chop the tree\n')
                    return False
            except Exception as e:
                print(e)

        elif func.function_code == 11:# Heal
            print("""Mmm..that was surprisingly good. You swallow...
A warmth spread over you. Check your Hp.""")
            self.regenerate(50)
            self.inventory.use_item(self.subject)

        elif func.function_code == 12:# Evade
            from random import randint
            if randint(0,100)<=func.var:
                return True
            else:
                return False

        elif func.function_code == 13:# Return
            return f'\n'

    def collect(self,items:item):
        print(f'You collected {str(items.amnt)}x{items.name}')
        print()
        self.inventory.add_inv(items)


