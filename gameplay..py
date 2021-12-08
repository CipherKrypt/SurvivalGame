"""The import statement uses the built in __import__() function
to search available paths for a file with name mentioned and import functions,
variables and classes from the .py file to the main code."""
from LifeForm import *

"""'from' imports mentioned functions from the file name preceded by it. '*' will import everything in the file"""

from Game_items import *

player=Player(500) # Initialize the Player Object as 'player'

def main_menu():
    """Prints the Main page and prompts for input...if user presses Enter it proceeds. If any other key is pressed...
    The program raises a SystemExit and terminates"""
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
                            luxurious island. Well on the way, your friends dared you to jump aboard... 
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
Yay -sarcasm-\n''')
            game_loop()
        else:
            raise SystemExit

def game_loop():
    """Game loops continuously checking if the player is dead,
    If dead it proceeds to GAME OVER message
    else continues to prompt the player for choice
    After a scout, the game goes through the cycle function."""
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
