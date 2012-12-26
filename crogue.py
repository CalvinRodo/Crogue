import sys
import libtcodpy as libtcod
from gobject import *
from di import DI
from map import Map
from MessageDisplay import *
import json
import copy

class Game(object):

  def __init__(self, font):
    self.di = DI()
    self.register_services()

    self.screen_height = 60
    self.screen_width = 100
    self.gamefont = sys.path[0] + '/data/fonts/' + font
    self.map = Map(80,45)
    self.fov_recompute = True
    #create the root console
    libtcod.console_set_custom_font(self.gamefont.encode('utf-8'), libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(self.screen_width, self.screen_height, 'crogue'.encode('utf-8'), False)

    #Create a console to draw to the screen
    self.con = libtcod.console_new(self.screen_width, self.screen_height)
    self.player = Player(self.map.starting_pos[0], self.map.starting_pos[1])
    self.objects = [self.player]

    self.Messages =  self.di.Request("Console")
    self.Messages.add_message("Game has been started.")

    self.load_monsters()
    self.add_monsters()
    self.add_items()

  def add_object_to_map(self, item):
    while True:
      y = libtcod.random_get_int(0, 0, self.map.height - 1)
      x = libtcod.random_get_int(0, 0, self.map.width - 1)
      if not self.map.is_blocked(x, y):
        break
    item.x = x
    item.y = y
    self.objects.append(item)

  def add_monsters(self):
    maxmonst = len(self.Monsters)  - 1
    for i in range(100):
      ind = libtcod.random_get_int(0,0,maxmonst)
      monster = copy.deepcopy(self.Monsters[ind])
      self.add_object_to_map(monster)

  def add_items(self):
    for i in range(100):
      self.add_object_to_map(Item(0,0))

  def handle_keys(self):
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:
      #Alt+Enter: toggle fullscreen
      libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
      return True  #exit game

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
      self.player.move(self.map,0,-1)
      self.fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
      self.player.move(self.map,0,1)
      self.fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
      self.player.move(self.map,-1,0)
      self.fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
      self.player.move(self.map,1,0)
      self.fov_recompute = True

  def render_all(self):
    self.render_timer1 = libtcod.sys_elapsed_milli()

    for object in self.objects:
      object.draw(self.con, self.map)

    if self.fov_recompute:
      #recompute FOV if needed (the player moved or something)
      self.fov_recompute = False
      self.map.recompute_fov(self.player.x, self.player.y)

    self.map.draw(self.con)

    messagePanel = self.Messages.render()

    libtcod.console_blit(messagePanel,
                         0, 0, self.Messages._maxWidth, self.Messages._maxHeight,
                         self.con, 0, 46)
    libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
    self.render_timer2 = libtcod.sys_elapsed_milli()

  def update_objects(self):
    self.update_timer1 = libtcod.sys_elapsed_milli()
    for object in self.objects:
      self.player.check_collision(object)
      if isinstance(object, Monster):
        if object.Alive is False:
          object.clear(self.con)
          self.objects.remove(object)
    self.update_timer2 = libtcod.sys_elapsed_milli()

  def main_loop(self):
    while not libtcod.console_is_window_closed():
      libtcod.console_set_default_foreground(self.con, libtcod.white)
      self.render_all()
      libtcod.console_flush()

      for object in self.objects:
        object.clear(self.con)

      exit = self.handle_keys()

      self.update_objects()

      self.render_timers()

      if exit:
        break

  def render_timers(self):
    updateTime = self.update_timer2 - self.update_timer1
    renderTime = self.render_timer2 - self.render_timer2
    libtcod.console_set_default_foreground(self.con, libtcod.white)
    libtcod.console_print(self.con,0,0,("Update Timer:  " + str(updateTime)).encode())
    libtcod.console_print(self.con,0,1,("Render Timer:  " + str(renderTime)).encode())

  def load_monsters(self):
    file = open("Monsters.json")
    monsterList = json.load(file)
    self.Monsters = []
    for m in monsterList["Monsters"]:
      self.Monsters.append(Monster.create_from_dict(m))

  def register_services(self):
    self.di.Register("Console", lambda: MessageDisplay())



g = Game('8x8.png')
g.main_loop()




