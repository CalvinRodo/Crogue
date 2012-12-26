import libtcodpy as libtcod
from di import DI

class GObject(object):
  #this is a generic object: the player, a monster, an item, the stairs...
  # it's always represented by a character on screen.
  def __init__(self, x, y, char, color):
    self.x = x
    self.y = y
    self.char = char
    self.color = color
    self.blocking = True

  #Do we block something from moving here?
  def blocks(self, obj,  x, y):
    if self.blocking == False:
     return False

    if (self.x == (obj.x + x) and self.y == (obj.y + y)):
      return True

    return False

  def move(self, map, dx, dy):
    #move by the given amount
    if not map.is_blocked(self.x + dx,self.y + dy):
      self.x += dx
      self.y += dy

  def draw(self, con, map):
    if map.is_pos_visible(self.x, self.y):
      #set the color and then draw the character that represents this object at its position
      libtcod.console_set_default_foreground(con, self.color)
      libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

  def clear(self, con):
    #erase the character that represents this object
    libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

class Player(GObject):
  def __init__(self, x,y):
    GObject.__init__(self,x,y,'@',libtcod.white)
    self.inventory = []

  def check_collision(self, object):
    if isinstance(object, Player):
      return
    if object.x != self.x or object.y != self.y:
      return
    if isinstance(object, Monster):
      object.Alive = False
      object.kill_message()
    if isinstance(object, Item):
      self.add_to_inventory(object)

  def add_to_inventory(self, item):
    self.inventory.append(item)
    item.in_container(True)

class Item(GObject):
  def __init__(self, x, y):
    GObject.__init__(self, x, y, 'i', libtcod.darkest_red)
    self.name = "Item"
    self.blocking = False

  def in_container(self,flag):
    self.in_inventory = flag

class Monster(GObject):
  def __init__(self,x,y):
    GObject.__init__(self,x,y,'m',libtcod.darkest_green)
    self.Alive = True
    self.blocking = True
    di = DI()
    self.Messages = di.Request("Console")

  def kill_message(self):
    self.Messages.add_message(self.Name + " was killed!")

  @staticmethod
  def create_from_dict(dict):
    m = Monster(0,0)
    m.Name = dict["Name"]
    m.Description = dict["Description"]
    m.char = dict["Tile"]
    return m