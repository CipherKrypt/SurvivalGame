from Environment import *
from Game_items import *

class Life():
    """Super class of Life form that will hold the max hp and current hp of characters"""
    def __init__(self,max_hp:int):
        self.max_hp=max_hp
        self.hp=max_hp

    def __str__(self) :
        return f'a Life form with Max HP: {self.max_hp} and Current HP: {self.hp}'

    def is_dead(self)-> bool:
        """Returns if the Life form is dead or not as a boolean value"""
        if self.hp<=0:
            return True
        else:
            return False

    def regenerate(self,hp_amnt):
        """Increases the hp of the lifeform by an amount given as a parameter"""
        if self.hp +hp_amnt>self.max_hp:
            self.hp =self.max_hp
        else:
            self.hp +=hp_amnt

    def hit(self,damage)-> bool:
        """Decreases the hp of the life form by na amount given as a parameter to simulate a hit and returns a boolean
        value of whether the Life Form is dead"""
        if self.hp-damage <=0:
            self.hp =0
        else:
            self.hp -=damage
        return self.is_dead()

class Exp():
    """A class Exp to hold experience of the player
    Initialize Current Xp, Xp needed to level up, Current Level"""
    def __init__(self):
        self.xp=1
        self.next_lvl=50
        self.lvl=1

    def __str__(self):
        return f'Level: {str(self.lvl)} XP: {str(self.xp)} Next Level in: {str(self.next_lvl-self.xp)}'

    def check_xp(self,lvl_up=False):
        """Function to check if player has leveled up and return Boolean value regarding the same"""
        if self.xp>=self.next_lvl:
            self.lvl+=1
            self.next_lvl*=2
            print(f'Woah! You Leveled Up... Level{str(self.lvl)}')
            lvl_up = True
        if self.xp<self.next_lvl:
            if lvl_up:
                return True
            else:
                return False
        else:
            self.check_xp(lvl_up)

    def add_xp(self,xp:float or int)-> bool:
        """Adds xp to player and returns boolean value regarding if the player has leveled up"""
        self.xp+=xp
        print(f'You got +{xp} XP!')
        return self.check_xp()



class Animal(Life):
    """Class Animal to hold the different animal objects
    Takes Max hp, Animal's name,Description,Drops"""
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
    """Class Tree to hold object Tree that takes number of wood to be dropped as parameter"""
    def __init__(self,wood:int):
        self.wood=wood
        self.is_cut=False

    def __str__(self):
        return f'a Tree object that will drop {self.wood} wood'


class Player(Life):
    """Class Player to hold Object player
    Takes in Max Hp, and initialize all other values
    Creates an inventory for the player
    Sets turn played as Zero
    Set's equiped Item as None
    Sets Hydration of the player as 10% of PLayer's HP
    Sets Energy of the player as 10% of Player's HP
    Sets EXP object as xp
    Sets subject [subject of player's action] as None
    Sets day survived as 1
    Sets the player's available action to scout and check inventory"""
    def __init__(self,max_hp):
        super().__init__(max_hp)
        self.inventory=self.premade_inventory()
        self.location:Location=self.premade_location('wild')
        self.turn = 0
        self.equip:item or None = None
        self.hydration = (self.hp)/10
        self.energy = (self.hp)/10
        self.xp = Exp()
        self.subject:Animal or item or Tree or None = None
        self.day = 1
        self.actions=moves(self.premade_function('scout'),self.premade_function('inventory'))

    def __str__(self):
        if self.equip == None:
            equiped='Nothing'
        else:
            equiped=self.equip.name
        return f'You:|Level: {str(self.xp.lvl)}|Xp:{str(int(self.xp.xp))}/{str(self.xp.next_lvl)}|\n' \
               f'|Hp: {str(self.hp)}/{str(self.max_hp)}|Hydration: {str(int(self.hydration))}/{str(int(self.max_hp/10))}|Energy: {str(self.energy)}/{str(int(self.max_hp/10))}|Equiped: {equiped}|'

    def cycle(self):
        """After a scouting expedition the player uses up a turn
         The cycle parameter checks the Player's vitals and prints the necessary message
         If 5 turns taken it changes the time to Night and increase the chance of finding wolves
         if 10 turns done, increments day survived by one resets the chance of finding wolves
         If 10 days survived, declares the player as Survived.
         Every turn this function heals the player, use up the player's Hydration and Energy."""
        print()
        if self.day == 10:
            self.game_over(Survived)
            return
        self.regenerate(10 + 10 * self.xp.lvl)
        print(f"You healed +{str(10 + 10 * self.xp.lvl)} HP")
        if self.turn==10:
            self.day+=1
            self.turn=1
            self.location.decrease_attribute('w', 30)
            print("Dawn arrives...A brand new day! but the same ol' routine -eye roll-\n")
        else:
            self.turn+=1
        if self.turn ==5:
            self.location.increase_attribute('w',30)
            print("It's dark ALREADY! -wood snaps- Wait! is that a wolf?\n")
        self.hydration-=4*self.location.thirst_mult
        if self.hydration<=0:
            self.game_over(DeathByDehydration)
            return
        if self.hydration<=30:
            print(f'(!) Your Hydaration is {str(self.hydration)}. You need Water stat! Keep it above 30 else you lose energy!')
            self.energy-=5
        self.energy-=2
        if self.energy>=50:
            self.regenerate(5*self.xp.lvl)
        if self.energy<=20:
            print(f'(!) Your Energy is {str(self.energy)}. You need Food stat! Keep it above 20 else you lose Hp!')
            if self.hit(5):
                self.game_over(DeathByStarvation)
                return
        if self.energy<=0:
            self.game_over(DeathByStarvation)
            return

        if self.hp <=100:
            print(f'(!)Your Hp is at a Critical Level. Only {str(self.hp)} HP left. Be careful! Try to Heal!')

    def get_ch(self):
        """This function updates the player's action variable and asks the player for the input and
        directs to the respective function depending on the player's choice"""
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
        """Takes in an Error and
        Depending the type of situation that triggered GAME OVER, this function will print a respective message"""
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
              """
                                                                  ____ ___  _ _    ____ ____ _  _ ____ 
                                                                  |___ |__] | |    |  | | __ |  | |___ 
                                                                  |___ |    | |___ |__| |__] |__| |___
                                                                  
                                                                  
                                                                            -soft buzz-
                                                    Oh no... is that a swarm of bees!? REALLY!? wolves and now this!...
                                              Yup...Moms do know best!! She did tell you to take a tube of insect repellent.
                                                          If only you had listened to your Mom and brought it...
                                                                        -buzz turns into roar-
                                                You look up... something like a huge bee is headed your direction...is it?...
                                                A Helicopter!!! It's landing by the beach! Finally someone came to save you!
                                                 You run towards it...braving the wind...shielding your eyes from the dust
                                                 One of the passenger hold out his hand....you reach out...you are saved -
                                                 
                                                                        -    GAME OVER   -
                                                                               Huh!?    
                                                   Where are you? It's pitch black? What's this 'GAME OVER' display??
                                                     You feel like your head is being pulled up! Argh! The Light!!!                                             
                                                    'Dear sir, please relax... you just experienced an immersive reality'
                                                              'My Imminent Reality!!! I'm going to die!?'
                                                     'No sir, Immersive Reality...like VR but... just more real' -winks-
                                             'But....Why am I here? Where's my family? Mom!! I need to tell here she was right!'
                                             'Don't worry sir...you are one of our many willing participants...you don't remember
                                             because you are disoriented. You will in due time. Anyway, please fill out a form 
                                             regarding your experience using IR, collect your payment and you can be on your way.'
                                                                            'Wait! I am paid!?' 
                                                'Ha! Yes sir... NOW you seem energetic -laughs- anyway...right this way'
                                               He opens a door for you. You clearly can't remember signing up for any IR...
                                              But well...you might remember it soon enough...Time to collect your payment.
                                                           You follow him... at least you are safe right?
                                                                              or are you....
                                                                              
                                                                              - THE END -
                                                                  
                                                         No animals were harmed during the creation of this game.
                                                    Any resemblance to any code in existance is purely a coincidence.
                                                                    
                                                               _______ _______ _______ _____  ______ _______
                                                              |     __|   _   |    |  |     \|   __ \       |
                                                              |__     |       |       |  --  |      <   -   |
                                                              |_______|___|___|__|____|_____/|___|__|_______|
                                                                  
                                        01110011 01110101 01100010 01101001 01101110 01110011 01110101 01110010 01100101 01110011 01101000
                                                                  """
                  )
        self.hp=0

    def help(self):
        """"Prints out the Help message for the player"""
        print('Help Menu:')
        print(f'''
        Your task in this game is to survive the open world for 10 days
        so that help can arrive...
        Each day is composed of 10 cycles. 5 cycles for Morning and 5 for Night.
        Beware of the Night! You are more likely to encounter wolves. Equip items that can ward them off.
        Your standing so far:
        {self.__str__()}
        Keep an eye on your Health, Hydration and Energy
        Every cycle you will lose your Hydration and Energy depending on the Location you are.
        You will also heal a certain amount of Hp depending on your Level.
        NOTE:
        if your Hydration goes below 20, you start losing Energy
        if your Energy goes below 30, you start losing HP
        and if your HP becomes 0.....well congratulations! Now you know how NOT to play this game.
        
        How to Play:
        Everytime you can make a choice...
        your options will be shown under 'Do you want to...'
        'Type In' the option name to proceed EXCEPT when choosing items in inventory...
        at that time enter the number assigned to the item.
        Your goal is to gain Xp and Level Up...
        Chopping down trees, Hunting Hen and Pig and Defeating Wolves will all give you 
        Xp and drops.
        
        Your Level:
        It will govern how much damage you can deal and how accurate you are.
        It will govern how likely you are to catch an animal
        it will govern how much HP you have and can heal every turn.
        It will govern how much wood, meat, gold and xp animals and trees will drop.
        
        Your Inventory:
        Everytime you choose 'check inventory' you will be shown your Inventory.
        When you select an item...everything about it will be displayed
        Keep an out for Attributes...they govern what you can do with items that you equip...
        Chopper: Allows you to chop down Trees
        Damage: Allows you to deal damage to Wolves
        Light: Allows you to ward of wolves. Makes it unlikely that you will encounter one.
        Fire: THis attribute will make the item consume wood per cycle
        
        Items:
        Animals and Trees drop useful items...such as Meat, Wood and Gold
        You can also find items while scouting such as healing berries and water
        
        Well...That's all the help I can offer you..
        Your journey ahead, is your own... What awaits you?
        Only time can tell......
        ''')

    def lvl_up(self):
        """If the player has leveled up, it will make the necessary changes to Max Hp, Hydration and Energy.
        It will also reset these values to the Max."""
        self.max_hp += 20*self.xp.lvl
        self.hp = self.max_hp
        print("HP renewed")
        max = int(self.max_hp/10)
        self.hydration = max
        print("Hydration renewed")
        self.energy = max
        print("Energy renewed")

    def equip_item(self,Item:item):
        """Allows player to equip Items"""
        self.equip=Item

    def premade_location(self,location_name:str)->Location:
        """Pre defined Location to be assigned"""
        if location_name == 'wild':
            location = Location('Wilderness', 1.25, 0, 10, 50, 50, 10, 30, 40, 20, 10, 20)
        else:
            return NotAnAttribute
        return location

    def premade_function(self,function_name:str)-> function:
        """Pre made functions that can be assigned to items"""
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
            fun = function('Eat',11,50)
        elif function_name == 'evade':
            escape=52-2*self.xp.lvl
            if escape <0:
                escape=0
            fun = function('Evaded',12,escape)
        elif function_name == 'return':
            fun = function('Return',13,0)
        elif function_name == 'shop':
            fun = function('Shop',14,0)
        elif function_name == 'buy':
            fun = function('Buy',15,0)
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

    def premade_item(self,item_name:str)-> item or shop:
        """Premade items that can be used through out the game as:
        Scouted items, Dropped items, or Items sold by the Merchant"""
        if item_name == 'water':
            Item = item('Water',5,'A Consumable that will give +5 Hydration',moves(self.premade_function('drink')),1)
        elif item_name == 'wood':
            Item = item('Wood',1,'Consumable dropped by trees...used as fuel for torches.',None,2)
        elif item_name == 'chicken':
            Item = item('Meat',1,'Consumable dropped by Hen and Pig that will give +5 Energy',moves(self.premade_function('eat')),1)
        elif item_name == 'pork':
            Item = item('Meat', 2, 'Consumable dropped by Hen and Pig that will give +5 Energy',moves(self.premade_function('eat')),1)
        elif item_name == 'axe':
            Item = item('Axe',1,'An item that can be equipped to cut down trees and maybe even deal some damage',moves(self.premade_function('equip'),self.premade_function('chopper'),self.premade_function('damage')),2)
        elif item_name == 'berry':
            Item = item('Berry',1,'A Consumable that will replenish give +50 Hp and +10 Energy',moves(self.premade_function('heal')),2)
        elif item_name == 'gold':
            Item = item('Gold',1,'Gold can be found or dropped by wolves. Use it to buy items from merchants',None,0)
        elif item_name == 'torch':
            Item = item('Torch',1,'An item that consumes 1xwood per cycle to provide fire and ward off Wolves when equiped',moves(self.premade_function('equip'),self.premade_function('light'),self.premade_function('fire')),4)
        elif item_name == 'taco':
            eat=self.premade_function('eat')
            eat.set_var(20)
            Item = item('Taco',1,'Consumable sold my the merchant...known to cause diarrhea...but also give +20 Energy',moves(eat),3)
        elif item_name == 'shop':
            Item = shop(self.premade_item('water'),self.premade_item('chicken'),self.premade_item('wood'),self.premade_item('berry'),self.premade_item('taco'),self.premade_item('torch'))
        else:
            return NotAnAttribute
        return Item

    def premade_inventory(self)-> inventory:
        """Premade Inventory that will be assigned to player at the start of the game"""
        invent = inventory(self.premade_item('axe'))
        return invent

    def premade_animal(self,animal_name:str) -> Animal:
        """Premade Animals that the player will encounter in a scout"""
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
        """This is where all the function codes assigned to function objects are read and the necessary game play executed"""
        if func.function_code == 1:#
            items=self.subject
            if items.sub_item():
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
            else:

                print("You look into your canteen, there is a drop left. You tip it your mouth\n"
                      "the drop falls...but on to your shirt...Darn it!")
            print()
            return False
        elif func.function_code == 2:# Eat
            items = self.subject
            if items.sub_item():
                max_val = self.max_hp / 10
                max_val = float(max_val)
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
            else:
                print("Your stomach's growling, you reach out into your bag for food...Nothing!!\n"
                      "that locust looks delicious... -disgusted by the thought-")
            print()
            return False
        elif func.function_code == 3:# Equip
            self.equip_item(self.subject)
            print(f'You equipped {self.subject.name}\n')
        elif func.function_code == 4:# Scout
            torch = False
            if self.equip != None:
                if 'light' in self.equip.att.list_it():
                    if self.inventory.use_item('Wood'):
                        print("1xWood used to fuel torch")
                        torch =True
                    else:
                        print("You don't have enough fuel for the torch")
            scouted=self.location.search()
            print('You start to scout the area...\n')
            found = False
            if scouted[8] and torch == False:#Attack by Wolf
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
                                    from random import randint,choice
                                    dam=randint(10*self.xp.lvl,30+10*self.xp.lvl)
                                    D=[0]
                                    for i in range(1+self.xp.lvl):
                                        D.append(dam)
                                    dam=choice(D)*self.equip.att[1].var
                                    print(f'You dealed {str(dam)} Damage.\n')
                                    if wolf.hit(dam):
                                        print(f'Phew! The wolf ran way....Woah it dropped {wolf.drops.content()}d !')
                                        if self.xp.add_xp((wolf.max_hp / 10)):
                                            self.lvl_up()
                                        self.collect(wolf.drops.collect(self.inventory))
                                        break
                                else:
                                    print('You need to equip something that can deal damage\n')
                                    continue
                            from random import choice
                            m:function=choice(list(wolf.move))
                            print(f'The wolf {m.name} you and dealt {str(m.var)} damage!\n')
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
                            continue
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
            if scouted[0]: # Merchant
                found = True
                print("\nMerchant: Hola Amigo!\n"
                      "          I have useful trinkets. Give you good price!\n"
                      "What! A Mexican Merchant! Way out here!? Are you saved!\n"
                      "It took only a few tries to understand that you just heard the only english he know.\n"
                      "-sigh- You are stuck here for longer... You look at him.\n"
                      "He is kinda shady... but maybe there is no harm in checking what he has...\n")
                while True:
                    try:
                        self.subject=self.premade_item('shop')
                        self.actions= moves(self.premade_function('shop'),self.premade_function('pass'))
                        if self.get_ch():
                            break
                    except:
                        pass
                    break
            if found:
                print("Phew! All in a days work...Now what to do?")
            else:
                print("Maaan! All that walking and you didn't find ANYTHING!? Try again")
            print()
            try:
                while True:
                    print('Do you want to...\n'
                          'end scout   check inventory')
                    print(self.__str__())
                    ch = input('Enter>> ')
                    ch = ch.lower().lstrip().rstrip()
                    if ch == 'check inventory':
                        self.enact(self.premade_function('inventory'))
                    elif ch == 'end scout':
                        return True
                    else:
                        continue
            except:
                return True
        elif func.function_code == 5:# Check Inventory
            while True:
                print("\n"
                  "Your Inventory\n"
                  "---------------")
                if self.inventory.content() == []:
                    print('-Nothing in Inventory-\n')
                    return False
                inv=self.inventory.list_inv()
                print('0. Exit')
                for i in range(len(inv)):
                    print(f'{str(i+1)}. {inv[i].name}')
                try:
                    ch = int(input('Enter item number>> '))
                    if ch == 0:
                        print()
                        return False
                    elif ch <= len(inv)+1:
                        items:item=self.inventory[ch-1]
                        self.subject = items
                        print(items)
                        try:
                            self.actions = moves(items.att[0], self.premade_function('return'))
                        except:
                            self.actions = moves(self.premade_function('return'))
                        self.get_ch()

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
                        print("Sheesh! It got away... Maybe next time.\n")
                        return True
                    else:
                        print(f'Here...buck.buck.buck.. -catches hen- Nice! got {animal.drops.content()}!')
                        if self.xp.add_xp(10):
                            self.lvl_up()
                        self.collect(animal.drops.collect(self.inventory))
                        return True

            if animal.animal == 'Pig':
                if self.enact(animal.move[0]):
                    print("Man! That pig was FAST!... So much for your bacon -eyeroll-.\n")
                    return True
                else:
                    print(f'If you move reeeaaalll slow, you might become invisible -catches pig- Cool! got {animal.drops.content()}!')
                    if self.xp.add_xp(10):
                        self.lvl_up()
                    self.collect(animal.drops.collect(self.inventory))
                    return True


        elif func.function_code == 7:# Refill
            print('Ah....That was a good drink. You fill your canteen\n')
            self.hydration = self.max_hp / 10
            self.regenerate(10)
            water = self.premade_item('water')
            water.set_amnt(5)
            self.inventory.add_inv(water)

        elif func.function_code == 8:# Pass
            print()
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
                if items.name == 'Wood':
                    print('Meh...Extra wood is just extra baggage...You can probably make do with what you got')
                if items.name == 'Gold':
                    print("Nah! It might be Fool's gold for all you know... You walk away... A FOOL!")
            if type(self.subject) == shop:
                print("Maybe not... the last thing you need is diarrhea from eating tacos. -shivers at the thought of it-\n"
                      "'Adios! strange Mexican merchant..' you walk away...")
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
                    print('\nHeave Ho! annnndddd.... Lumber!\n')
                    self.xp.add_xp(2)
                    wood.set_amnt(wood.amnt * m)
                    self.inventory.add_inv(wood)
                    return True
                else:
                    print('You need to equip something that has chopper attribute,to chop the tree\n')
                    return False
            except Exception as e:
                print(e)

        elif func.function_code == 11:# Heal
            if self.subject.sub_item():
                print("""Mmm..that was surprisingly good. You swallow...
    A warmth spread over you. Check your Hp.\n""")
                self.regenerate(50)
                print("+50 HP")
                max_val=self.max_hp/10
                if self.energy+10 >= max_val:
                    self.energy = max_val
                    print("Energy renewed")
                else:
                    self.energy += 10
                    print("+10 Energy")

        elif func.function_code == 12:# Evade
            from random import randint
            if randint(0,100)<=func.var:
                return True
            else:
                return False

        elif func.function_code == 13:# Return
            return True

        elif func.function_code == 14:# Shop
            Shop = self.subject
            while True:
                print(Shop)
                try:
                    gold=self.inventory['gold']
                    print(f"Your Gold: {gold.amnt}")
                except:
                    print("Your Gold: 0")
                try:
                    ch = int(input('Enter item number>> '))
                    if ch == 0:
                        print("\n")
                        return False
                    elif ch<= len(Shop.list_it()):
                        while True:
                            items= Shop[ch-1]
                            print("\n"
                                  f"Item Name: {items.name}\n"
                                  f"Description: {items.desc}\n"
                                  f"Cost: {items.cost} Gold pieces\n")
                            self.subject = items
                            self.actions = moves(self.premade_function('buy'),self.premade_function('return'))
                            if self.get_ch():
                                break
                except:
                    pass

        elif func.function_code == 15: # Buy
            items = self.subject
            if self.inventory.use_item('gold',items.cost):
                print("Ka-Ching! The deals been done!\n")
                items.set_amnt(1)
                self.inventory.add_inv(items)
                return False
            else:
                print(f"Merchant:Oye Amigo! you don't have enough gold.\n")
                return True

    def collect(self,items:item):
        """Adds Items dropped by animals and scouted items into the Players inventory."""
        print()
        self.inventory.add_inv(items)


