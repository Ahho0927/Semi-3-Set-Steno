from pynput.keyboard import Key, Listener, Controller
from keyboard import write

def on_press(key: Key) -> None:
    if key == Key.esc:
        return False
    
    print(key, True)

def on_release(key: Key) -> None:
    print(key, False)


if __name__ == '__main__':
    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()