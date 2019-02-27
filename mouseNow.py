#! python3
# mouseNow.py
import pyautogui,time

while True:
    x, y = pyautogui.position()
    pixel_color = pyautogui.screenshot().getpixel((x, y))
    position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    position_str += '  RGB('
    for col in pixel_color:
        position_str += ' ' + str(col).rjust(3)
    position_str += ')'
    print(position_str)
    time.sleep(1)

