from os import system

from data.keyboard import *

def text():
    """
    A Title Display.
    """
    system('cls')
    print('''

 ██████╗  ██████╗  ██████╗  ██╗ ██████╗   █████╗   ██╗   ██╗   █████╗ 
██╔════╝ ██╔═══██╗ ██╔══██╗ ██║ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██╔══██╗
 █████╗  ██║   ██║ ██████╔╝ ██║ ██║  ██║ ███████║ ██╔████╔██║ ███████║
╚════██║ ██║   ██║ ██╔══██╗ ██║ ██║  ██║ ██╔══██║ ██║╚██╔╝██║ ██╔══██║
██████║  ╚██████╔╝ ██║  ██║ ██║ ██████╔╝ ██║  ██║ ██║ ╚═╝ ██║ ██║  ██║
╚═════╝   ╚═════╝  ╚═╝  ╚═╝ ╚═╝ ╚═════╝  ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚═╝  ╚═╝
          
          ''')


# #################################################################

keyboard = Keyboard()
if __name__ == '__main__':
    text()
    keys.block_keys(keys.KEY_BLOCKED)
    with Listener(on_press=keyboard.on_press, on_release=keyboard.on_release) as listener:
        listener.join()