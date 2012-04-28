import libtcodpy as libtcod
from map import Map

class GObject(object):
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
 
    def move(self, map, dx, dy):
        #move by the given amount
        if not map.is_blocked(self.x + dx,self.y + dy):
            self.x += dx
            self.y += dy
 
    def draw(self, con, map):        
        if map.is_pos_visible(self.x, self.y):    
            #set the color and then draw the character that represents this object at its position
            libtcod.console_set_foreground_color(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)
 
    def clear(self, con):
        #erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)