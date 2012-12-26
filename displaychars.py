from _ctypes import Array
import sys

__author__ = 'calvin'
import libtcodpy
length = 45

gamefont = sys.path[0] + '/data/fonts/8x8.png'
libtcodpy.console_set_custom_font(gamefont.encode('utf-8'), libtcodpy.FONT_TYPE_GREYSCALE | libtcodpy.FONT_LAYOUT_ASCII_INROW)
libtcodpy.console_init_root(length,length,"Ascii Chars of Tiles".encode())
libtcodpy.console_set_default_foreground(0, libtcodpy.white)

x = 0
y = 0

for i in range(256):
  if i == 6:
    continue
  key = "".join([str(i),": ",chr(i)])
  libtcodpy.console_print(0, x, y, key)
  y += 1
  if y == length:
    x += 7
    y = 0

libtcodpy.console_flush()
libtcodpy.console_wait_for_keypress(True)
