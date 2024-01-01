from pynput.keyboard import Key, Listener
from keyboard import unhook_all

from data.translation import Translation
from data.key import Keys
from data.VKCODE import *

translation = Translation()
keys = Keys()

class Keyboard:
    def __init__(self) -> None:
        self.currently_pressed_key = set()
        self.currently_pressed_modifier_key = set()
        self.pressed_key = set()
        self.is_running: bool = True

    def on_press(self, key: Key) -> None:
        """A function that runs when any key is pressed(on).

        Args:
            key (Key): The pressed key.
        """
        try:
            key: str = key.char
        except:
            pass

        if key == Key.space:
            key = 'space'
        if self.is_running and key in keys.KEY_USED and keys.key_sent[key] == 0:
            self.currently_pressed_key.add(key)
            self.pressed_key.add(key)

        elif key == Key.esc and (Key.shift in self.currently_pressed_modifier_key
                               or Key.shift_l in self.currently_pressed_modifier_key
                               or Key.shift_r in self.currently_pressed_modifier_key):
            return False # End Program
        
        elif key == Key.f6:
            translation.__init__()
        
        elif key in keys.MODIFIER_KEY:
            self.currently_pressed_modifier_key.add(key)

    def on_release(self, key: Key) -> None:
        """A function that runs when any key is released(off).

        Args:
            key (Key): The released key.
        """
        try:
            key = key.char
        except:
            pass

        if key == Key.f7:
            self.is_running = not self.is_running
            unhook_all()
            if self.is_running:
                keys.block_keys(keys.KEY_BLOCKED)
        else:
            try:
                if key == Key.space:
                    key = 'space'
                if self.is_running and key in keys.KEY_USED:
                    if keys.key_sent[key] == 0:
                        self.currently_pressed_key.remove(key)
                    
                        if len(self.currently_pressed_key) == 0: # End Stroke
                            self.result = translation.indicator_to_result(translation.key_to_string_indicator(self.pressed_key))
                            
                            translation.previous += self.result
                            if len(translation.previous) >= 10:
                                translation.previous = translation.previous[-10:]

                            keys.PressReleaseKeys(translation.transform_to_keys(self.result), translation.backspace_pressed_count)

                            self.stroke_reset()

                    elif keys.key_sent[key] != 0:
                        keys.key_sent[key] -= 1
            
                elif key in keys.MODIFIER_KEY:
                    self.currently_pressed_modifier_key.remove(key)

                elif key == Key.backspace:
                    translation.reset_previous()

                elif key in [Key.f9, Key.f10, Key.f11, Key.f12]:
                    translation.reset_previous()
                    unhook_all()
                    match key:
                        case Key.f9:
                            keys.PressReleaseKey(VK_LEFT)
                        case Key.f10:
                            keys.PressReleaseKey(VK_UP)
                        case Key.f11:
                            keys.PressReleaseKey(VK_DOWN)
                        case Key.f12:
                            keys.PressReleaseKey(VK_RIGHT)
                    keys.block_keys(keys.KEY_BLOCKED)

            except KeyError:
                pass
    
    def stroke_reset(self) -> None:
        self.pressed_key = set()