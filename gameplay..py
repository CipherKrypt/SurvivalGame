from LifeForm import *
from Game_items import *

player=Player(500)
'''
#print(wild.__str__())
Life=Life(100)
#print(Life)
eat=function('Eat',2,5)
roast=function('Roast and Eat',2,10)
food=moves(eat,roast)
#print(food)
Item=item('Pork',2,'Consumable that will replenish Energy',food)
Drop=drop(Item)
pig=Animal(100,'Pig','An animal with the chance to drop consumables',Drop)
player=Player(500,wild)
print(player)
#print(player)
'''
def main_menu():
    print('''
    
        :'######::'##::::'##:'########::'##::::'##:'####:'##::::'##::::'###::::'##::::::::'######::::::'###::::'##::::'##:'########:
        '##... ##: ##:::: ##: ##.... ##: ##:::: ##:. ##:: ##:::: ##:::'## ##::: ##:::::::'##... ##::::'## ##::: ###::'###: ##.....::
         ##:::..:: ##:::: ##: ##:::: ##: ##:::: ##:: ##:: ##:::: ##::'##:. ##:: ##::::::: ##:::..::::'##:. ##:: ####'####: ##:::::::
        . ######:: ##:::: ##: ########:: ##:::: ##:: ##:: ##:::: ##:'##:::. ##: ##::::::: ##::'####:'##:::. ##: ## ### ##: ######:::
        :..... ##: ##:::: ##: ##.. ##:::. ##:: ##::: ##::. ##:: ##:: #########: ##::::::: ##::: ##:: #########: ##. #: ##: ##...::::
        '##::: ##: ##:::: ##: ##::. ##:::. ## ##:::: ##:::. ## ##::: ##.... ##: ##::::::: ##::: ##:: ##.... ##: ##:.:: ##: ##:::::::
        . ######::. #######:: ##:::. ##:::. ###::::'####:::. ###:::: ##:::: ##: ########:. ######::: ##:::: ##: ##:::: ##: ########:
        :......::::.......:::..:::::..:::::...:::::....:::::...:::::..:::::..::........:::......::::..:::::..::..:::::..::........::


                        ___  ____ ____ ____ ____   ____ _  _ ___ ____ ____   ___ ____   ___  _    ____ _   _ 
                        |__] |__/ |___ [__  [__    |___ |\ |  |  |___ |__/    |  |  |   |__] |    |__|  \_/  
                        |    |  \ |___ ___] ___]   |___ | \|  |  |___ |  \    |  |__|   |    |___ |  |   |  
''')

    while True:
        ch=input('')
        ch = ch.lower().lstrip().rstrip()
        if ch == '':
            print('''
                                              ___  ____ ____ _    ____ ____ _  _ ____ 
                                              |__] |__/ |  | |    |  | | __ |  | |___ 
                                              |    |  \ |__| |___ |__| |__] |__| |___
                            _________________________________________________________________________
                                                     -you open your eyes-
                               'Wait? Where are am I?...Ack! what's in my mouth -spits out sand-'
                                   You are so confused...That's when your memory rushed back!
                               You signed up for a cruise...A trip on a luxury ship going to a 
                              luxurious island. Well on way, your friends dared to jump aboard... 
                                          swim a while and board the ship again.
                                    You are a pretty strong swimmer. So...why not?
                                But what you didn't expect is the current to be so...strong.
                                                  It pulled you under...
                              Your friends expected you to pop up any moment... You never did...
                              The waves pulled you further and further away from your ship. 
                                    All you could remember after that is pure panic.
                                                   Now you are here... 
                             You pick an old rusty axe... fashion a canteen out of leaves
                                 Now all you need do is to survive till help arrives.
                            And if you die along the way... Well at least you got to go to an island
                                                 not a Luxurious one though....
                    
                                    <type in 'help' or '!h' anytime to pull up the Help Menu>
                            ---------------------------------------------------------------------------
            

It's bright out here...
You better find water and food soon
There are probably wild animals too...
Yay -sarcasm-''')
            game_loop()
        else:
            raise SystemExit

def game_loop():
    while not player.is_dead():
        try:
            player.actions = moves(player.premade_function('scout'),player.premade_function('inventory'))
            if player.get_ch():
                player.cycle()
        except:
            pass
    print(f'''
    You survived for {str(player.day)} Day with a Level of {str(player.xp.lvl)}
                     -GAME OVER-
    ''')
    main_menu()


main_menu()
