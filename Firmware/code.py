import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules import Module

keyboard = KMKKeyboard()

# Switch pins
switch_pins = [board.D7, board.D11, board.D10, board.D9, board.D8]

keyboard.matrix = KeysScanner(
    pins=switch_pins,
    value_when_pressed=False  # pull-ups
)

keyboard.keymap = [
    [KC.A, KC.B, KC.C, KC.D, KC.E]
]

# LEDs
led1 = digitalio.DigitalInOut(board.D5)
led1.direction = digitalio.Direction.OUTPUT

# Rotary encoder pins
pin_a = digitalio.DigitalInOut(board.GP2)
pin_a.direction = digitalio.Direction.INPUT
pin_a.pull = digitalio.Pull.UP

pin_b = digitalio.DigitalInOut(board.GP1)
pin_b.direction = digitalio.Direction.INPUT
pin_b.pull = digitalio.Pull.UP

pin_sw = digitalio.DigitalInOut(board.GP3)
pin_sw.direction = digitalio.Direction.INPUT
pin_sw.pull = digitalio.Pull.UP
# led2 = digitalio.DigitalInOut(board.D6)
# led2.direction = digitalio.Direction.OUTPUT
class RotaryLetter(Module):
    """Allow use of the rotary encoder"""
    def __init__(self):
        self.position = 0  # current selected letter index
        self.last_a = pin_a.value
        self.letters = (KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G, KC.H, KC.I, KC.J, KC.K, KC.L, KC.M, KC.N, KC.O, KC.P, KC.Q, KC.R, KC.S, KC.T, KC.U, KC.V, KC.W, KC.X, KC.Y, KC.Z)

    def on_matrix_scan(self, keyboard, _, **_kwargs):
        # Read encoder rotation
        a_val = pin_a.value
        b_val = pin_b.value
        if a_val != self.last_a:
            if b_val != a_val:
                self.position += 1
            else:
                self.position -= 1
            # Wrap around
            self.position %= len(self.letters)
            print("Rotary position:", self.position)
        self.last_a = a_val

        # Check button press
        if not pin_sw.value and not getattr(self, "sw_last", False):
            keyboard.press(self.letters[self.position])
            keyboard.release_all()
#led1.value = True
led1.value = False

def led_hook(_, pressed):
    """Turn on LED1 when a key is pressed, turn off when released"""
    led1.value = pressed

rotary = RotaryLetter()
keyboard.modules.append(rotary)

keyboard.on_key_press = led_hook

# Start keyboard
if __name__ == "__main__":
    keyboard.go()