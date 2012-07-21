import libtcodpy as libtcod

class Tile(object):
  #a tile of the map and its properties
  def __init__(self, blocked, block_sight = None):

    self.blocked = blocked
    #by default, if a tile is blocked, it also blocks sight
    if block_sight is None: block_sight = blocked

    self.block_sight = block_sight

    self.color_dark_wall = libtcod.Color(0, 0, 100)
    self.color_light_wall = libtcod.Color(130, 110, 150)
    self.color_dark_ground = libtcod.Color(50, 50, 150)
    self.color_light_ground = libtcod.Color(200, 180, 50)

  def get_colour(self, visible):
    if visible:
      if self.blocked:
        return self.color_light_wall
      return self.color_light_ground
    if self.blocked:
      return self.color_dark_wall
    return self.color_dark_ground