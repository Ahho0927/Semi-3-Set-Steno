from pynput.keyboard import Key, Controller
from keyboard import block_key, unhook_all
import ctypes
from data.VKCODE import *

KEYBD_LAYOUT = '''
           ESC  F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12
           `  1  2  3  4  5  6  7  8  9  0  -  =  BACK
           TAB  Q  W  E  R  T  Y  U  I  O  P  [  ]  \ 
           CAPS A  S  D  F  G  H  J  K  L  ;  '  ENTER
           SHIFT  Z  X  C  V  B  N  M  ,  .  /  RSHIFT
           CTRL CMD         SPACE            MENU CTRL
           '''

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))
class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))
class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))
    

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
                         'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'space']

        self.KEY_BLOCKED = ['f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 
                            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
                            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[',
                            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",
                            'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'space']

        self.MODIFIER_KEY = [Key.shift, Key.shift_l, Key.shift_r, 
                             Key.ctrl, Key.ctrl_l, Key.ctrl_r, 
                             Key.alt, Key.alt_gr, Key.alt_l, Key.alt_r, 
                             Key.cmd, Key.cmd_l, Key.cmd_r]
        
        self.KEY_TO_VKCODE: dict[str, int] = {'`': VK_OEM_3, '1': KEY_1, '2': KEY_2, '3': KEY_3, '4': KEY_4, '5': KEY_5, '6': KEY_6, '7': KEY_7, '8': KEY_8, '9': KEY_9, '0': KEY_0, '-': VK_OEM_MINUS, '=': VK_OEM_PLUS, 
                                              'q': KEY_Q, 'w': KEY_W, 'e': KEY_E, 'r': KEY_R, 't': KEY_T, 'y': KEY_Y, 'u': KEY_U, 'i': KEY_I, 'o': KEY_O, 'p': KEY_P, '[': VK_OEM_4, ']': VK_OEM_6, '\\': VK_OEM_5, 
                                              'a': KEY_A, 's': KEY_S, 'd': KEY_D, 'f': KEY_F, 'g': KEY_G, 'h': KEY_H, 'j': KEY_J, 'k': KEY_K, 'l': KEY_L, ';': VK_OEM_1, "'": VK_OEM_7, 
                                              'z': KEY_Z, 'x': KEY_X, 'c': KEY_C, 'v': KEY_V, 'b': KEY_B, 'n': KEY_N, 'm': KEY_M, ',': VK_OEM_COMMA, '.': VK_OEM_PERIOD, '/': VK_OEM_2,
                                              VK_SPACE: VK_SPACE}

        self.INPUT_MOUSE = 0
        self.INPUT_KEYBOARD = 1
        self.INPUT_HARDWARE = 2
        
        self.KEY_UPPER = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
        self.KEY_LOWER = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
        self.KEY_UPPER_TO_LOWER = dict(zip(self.KEY_UPPER, self.KEY_LOWER))
        
        self.key_sent: dict[str] = {key: 0 for key in self.KEY_USED}
        self.key_sent.update({'shift': 0, 'space': 0, VK_SPACE: 0})
        
    def _KeybdInput(self, code, flags):
        return KEYBDINPUT(code, code, flags, 0, None)

    def _Keyboard(self, code, flags=0):
        return self._Input(self._KeybdInput(code, flags))

    def _Input(self, structure):
        if isinstance(structure, MOUSEINPUT):
            return INPUT(self.INPUT_MOUSE, _INPUTunion(mi=structure))
        if isinstance(structure, KEYBDINPUT):
            return INPUT(self.INPUT_KEYBOARD, _INPUTunion(ki=structure))
        if isinstance(structure, HARDWAREINPUT):
            return INPUT(self.INPUT_HARDWARE, _INPUTunion(hi=structure))
        raise TypeError('Cannot create INPUT structure!')

    def block_keys(self, keys) -> None:
        for key in keys:
            block_key(key)

    def _PressKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = _INPUTunion()
        ii_.ki = KEYBDINPUT( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
        ##scancode
        #ii_.ki = KEYBDINPUT( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = INPUT( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def _ReleaseKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = _INPUTunion()
        ii_.ki = KEYBDINPUT( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
        ##scancode
        #ii_.ki = KEYBDINPUT( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = INPUT( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    def PressReleaseKey(self, KeyCode):
        self._PressKey(KeyCode)
        self._ReleaseKey(KeyCode)

    def PressReleaseBackspace(self, count=0):
        for c in range(count):
            Controller().press(Key.backspace)
            Controller().release(Key.backspace)

    def SendInput(self, *inputs):
        nInputs = len(inputs)
        LPINPUT = INPUT * nInputs
        pInputs = LPINPUT(*inputs)
        cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
        return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)
            
    def PressReleaseKeys(self, inputs: str):
        unhook_all()

        for key in inputs:
            if key == ' ':
                key = VK_SPACE
                self.key_sent['space'] += 1
            elif key in self.KEY_UPPER:
                self._PressKey(VK_LSHIFT)
                key = self.KEY_UPPER_TO_LOWER.get(key, key)
                self.key_sent['shift'] += 1
            self.PressReleaseKey(self.KEY_TO_VKCODE.get(key, 0))
            self._ReleaseKey(VK_LSHIFT)

            self.key_sent[key] += 1

        self.block_keys(self.KEY_BLOCKED)

    def otherKeys(self, key):
        if key in [Key.f9, Key.f10, Key.f11, Key.f12]:
            unhook_all()
            match key:
                case Key.f9:
                    self.PressReleaseKey(VK_LEFT)
                case Key.f10:
                    self.PressReleaseKey(VK_UP)
                case Key.f11:
                    self.PressReleaseKey(VK_DOWN)
                case Key.f12:
                    self.PressReleaseKey(VK_RIGHT)
            self.block_keys(self.KEY_BLOCKED)