from pynput.keyboard import Key, Controller
from keyboard import block_key, unhook_all

KEYBD_LAYOUT = '''
           ESC  F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12
           `  1  2  3  4  5  6  7  8  9  0  -  =  BACK
           TAB  Q  W  E  R  T  Y  U  I  O  P  [  ]  \ 
           CAPS A  S  D  F  G  H  J  K  L  ;  '  ENTER
           SHIFT  Z  X  C  V  B  N  M  ,  .  /  RSHIFT
           CTRL CMD         SPACE            MENU CTRL
           '''


class Keys:
    def __init__(self) -> None:
        self.KEYS: list[str] = [Key.esc, Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12, 
                        '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', Key.backspace, 
                        Key.tab, 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\', 
                        Key.caps_lock, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", Key.enter, 
                        Key.shift_l, 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', Key.shift_r, 
                        Key.ctrl_l, Key.cmd_l, Key.alt_l, Key.space, Key.alt_r, Key.cmd_r, Key.menu,
                        Key.shift, Key.ctrl, Key.cmd, Key.alt, Key.alt_gr]

        self.KEY_USED = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
                    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\', 
                    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",
                    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', Key.space]

        self.KEY_BLOCKED = ['f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 
                    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
                    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[',
                    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",
                    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'space']

        self.MODIFIER_KEY = [Key.shift, Key.shift_l, Key.shift_r, 
                        Key.ctrl, Key.ctrl_l, Key.ctrl_r, 
                        Key.alt, Key.alt_gr, Key.alt_l, Key.alt_r, 
                        Key.cmd, Key.cmd_l, Key.cmd_r]

        self.UPPER = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
        self.LOWER = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
        self.UPPER_TO_LOWER: dict[str] = dict(zip(self.UPPER, self.LOWER))

        self.key_sent: dict[str] = {key: 0 for key in self.LOWER}
        self.key_sent.update({Key.shift : 0, Key.space : 0})

    def block_keys(self, keys) -> None:
        for key in keys:
            block_key(key)

    def _PressKey(self, Key: Key):
        Controller().press(Key)

    def _ReleaseKey(self, Key: Key):
        Controller().release(Key)
    
    def PressReleaseKey(self, Key):
        self._PressKey(Key)
        self._ReleaseKey(Key)

    def PressReleaseBackspace(self, count=0):
        for c in range(count):
            Controller().press(Key.backspace)
            Controller().release(Key.backspace)
            
    def SendString(self, keys: str) -> None:
        """A function that sends inputs of the string to keyboard.

        Args:
            string (str): string(keys) to be sent
        """
        unhook_all()
        for key in keys:

            if key in self.UPPER:
                key = self.UPPER_TO_LOWER.get(key, '')
                Controller().press(Key.shift)
            if key == ' ':
                key = Key.space
            self.PressReleaseKey(key)
            Controller().release(Key.shift)

            self.key_sent[key] += 1
            
        self.block_keys(self.KEY_BLOCKED)


    def otherKeys(self, key):
        if key in [Key.f9, Key.f10, Key.f11, Key.f12]:
            unhook_all()
            match key:
                case Key.f9:
                    self.PressReleaseKey(Key.left)
                case Key.f10:
                    self.PressReleaseKey(Key.up)
                case Key.f11:
                    self.PressReleaseKey(Key.down)
                case Key.f12:
                    self.PressReleaseKey(Key.right)
            self.block_keys(self.KEY_BLOCKED)