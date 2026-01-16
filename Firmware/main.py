import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.RGB import RGB
from kmk.extensions.display import Display, SSD1306

keyboard = KMKKeyboard()

# --- Key Pins (Direkt-Pins) ---
# Reihenfolge wie von dir gewünscht:
# SW6(GP27), SW9(GP28), SW8(GP0), SW1(GP1), SW4(GP2), Encoder-S1(GP26)
keyboard.key_pins = (
    board.GP27, board.GP28, board.GP0, board.GP1, board.GP2, board.GP26
)

# --- Encoder Setup ---
encoder_handler = EncoderHandler()
# Pin A = GP4 (Pin 10), Pin B = GP3 (Pin 11)
# Da S1/S2 kein GND-Bezug hat, behandeln wir S1 oben als normalen Key-Pin
encoder_handler.pins = (
    (board.GP4, board.GP3, None, False),
)
keyboard.modules.append(encoder_handler)

# --- RGB Setup ---
# DIN ist laut vorherigem Bild an GP29
rgb = RGB(pixel_pin=board.GP29, num_pixels=2)
keyboard.extensions.append(rgb)

# --- Display Setup (OLED 0.91" 128x32) ---
# SDA = GP6 (Pin 5), SCL = GP7 (Pin 6)
i2c_bus = busio.I2C(board.D7, board.D6)
display_driver = SSD1306(i2c=i2c_bus, device_address=0x3C, width=128, height=32)
display = Display(display_driver)
keyboard.extensions.append(display)

# --- Keymap ---
# Index 0-4 sind deine Taster, Index 5 ist der Encoder-Push (S1)
keyboard.keymap = [
    [
        KC.A,        # SW6
        KC.B,        # SW9
        KC.C,        # SW8
        KC.D,        # SW1
        KC.E,        # SW4
        KC.MUTE,     # Encoder Push (GP26)
    ]
]

# Encoder Drehung: Rechts = Lauter, Links = Leiser
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD),),
]

if __name__ == '__main__':
    keyboard.go()