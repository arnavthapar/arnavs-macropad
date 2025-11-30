import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC

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

# led2 = digitalio.DigitalInOut(board.D6)
# led2.direction = digitalio.Direction.OUTPUT

#led1.value = True
led1.value = False

def led_hook(_, pressed):
    """Turn on LED1 when a key is pressed, turn off when released"""
    led1.value = pressed

keyboard.on_key_press = led_hook

# Start keyboard
if __name__ == "__main__":
    keyboard.go()