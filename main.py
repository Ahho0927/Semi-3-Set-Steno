from os import system
from pynput.keyboard import Key, Listener
from keyboard import unhook_all

from translation import Translation
from key_slower import Keys


# #################################################################
def text():
    system('cls')
    print('''

███████╗  ██████╗  ██████╗  ██╗ ██████╗   █████╗  ███╗   ███╗  █████╗ 
██╔════╝ ██╔═══██╗ ██╔══██╗ ██║ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██╔══██╗
███████╗ ██║   ██║ ██████╔╝ ██║ ██║  ██║ ███████║ ██╔████╔██║ ███████║
╚════██║ ██║   ██║ ██╔══██╗ ██║ ██║  ██║ ██╔══██║ ██║╚██╔╝██║ ██╔══██║
███████║ ╚██████╔╝ ██║  ██║ ██║ ██████╔╝ ██║  ██║ ██║ ╚═╝ ██║ ██║  ██║
╚══════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝ ╚═════╝  ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚═╝  ╚═╝
          
          ''')

class Keyboard:
    def __init__(self) -> None:
        text()
        self.currently_pressed_key = set()
        self.currently_pressed_modifier_key = set()
        self.pressed_key = set()
        self.is_running = True

    def on_press(self, key: Key) -> None:
        """A function that runs when any key is pressed(on).

        Args:
            key (Key): The pressed key.
        """
        try:
            key = key.char
        except:
            pass

        if key == Key.esc and (Key.shift in self.currently_pressed_modifier_key
                               or Key.shift_l in self.currently_pressed_modifier_key
                               or Key.shift_r in self.currently_pressed_modifier_key):
            return False # End Program
        
        elif key == Key.f6:
            translation.__init__()
        
        elif key in keys.MODIFIER_KEY:
            self.currently_pressed_modifier_key.add(key)

        elif self.is_running and key in keys.KEY_USED and keys.key_sent[key] == 0:
            self.currently_pressed_key.add(key)
            self.pressed_key.add(key)

        else:
            keys.otherKeys(key)

    def on_release(self, key: Key) -> None:
        """A function that runs when any key is released(off).

        Args:
            key (Key): The released key.
        """
        try:
            key = key.char
        except:
            pass

        try:
            if key in keys.key_sent and keys.key_sent[key] != 0:
                keys.key_sent[key] -= 1

            elif key == Key.f7:
                self.is_running = not self.is_running
                unhook_all()
                if self.is_running:
                    keys.block_keys(keys.KEY_BLOCKED)
            
            elif key in keys.MODIFIER_KEY:
                self.currently_pressed_modifier_key.remove(key)

            elif self.is_running and key in keys.KEY_USED:
                try:
                    self.currently_pressed_key.remove(key)
                except KeyError:
                    pass
            
                if len(self.currently_pressed_key) == 0: # End Stroke
                    self.result = translation.indicator_to_result(translation.key_to_string_indicator(self.pressed_key))
                    
                    translation.previous += self.result
                    if len(translation.previous) >= 10:
                        translation.previous = translation.previous[-10:]

                    keys.PressReleaseBackspace(translation.backspace_pressed_count)
                    keys.SendString(translation.transform_to_keys(self.result))

                    self.stroke_reset()
        except KeyError:
            pass
    
    def stroke_reset(self) -> None:
        self.pressed_key = set()


# #################################################################

keyboard = Keyboard()
translation = Translation()
keys = Keys()
if __name__ == '__main__':
    keys.block_keys(keys.KEY_BLOCKED)
    with Listener(on_press=keyboard.on_press, on_release=keyboard.on_release) as listener:
        listener.join()