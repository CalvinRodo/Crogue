import libtcodpy as libtcod
from rect import Rect
from tile import Tile

class Map(object):
  def __init__(self,width, height):
    self.height = height
    self.width = width

    self.room_max_size = 10
    self.room_min_size = 6
    self.max_rooms = 30
    self.fov_algo = 0  #default FOV algorithm
    self.fov_light_walls = True
    self.torch_radius = 10
    self.room_max_size = 10
    self.room_min_size = 6
    self.max_rooms = 30
    self.fov_algo = 0  #default FOV algorithm
    self.fov_light_walls = True
    self.torch_radius = 10
    self.make_map()
    self.make_fovmap()

  def make_fovmap(self):
    self.fov_map = libtcod.map_new(self.width, self.height)
    for y in range(self.height):
      for x in range(self.width):
        libtcod.map_set_properties(self.fov_map, x, y, not self.map[x][y].block_sight, not self.map[x][y].blocked)

  def make_map(self):
    #fill map with "blocked" tiles
    self.map = [[ Tile(True)
      for y in range(self.height) ]
        for x in range(self.width) ]

    #create two rooms
    rooms = []
    num_rooms = 0

    for r in range(self.max_rooms):
      #random width and height
      w = libtcod.random_get_int(0, self.room_min_size, self.room_max_size)
      h = libtcod.random_get_int(0, self.room_min_size, self.room_max_size)
      #random position without going out of the boundaries of the map
      x = libtcod.random_get_int(0, 0, self.width - w - 1)
      y = libtcod.random_get_int(0, 0, self.height - h - 1)

      #"Rect" class makes rectangles easier to work with
      new_room = Rect(x, y, w, h)

      #run through the other rooms and see if they intersect with this one
      #if we find an intersection we need to generate a new room

#      if len(list(filter(new_room.intersect, rooms))) > 0:
#        continue

      #"paint" it to the map's tiles
      self.create_room(new_room)

      #center coordinates of new room, will be useful later
      (new_x, new_y) = new_room.center()

      if num_rooms == 0:
        #this is the first room, where the player starts at
        self.starting_pos = (new_x, new_y)
      else:
        #all rooms after the first:
        #connect it to the previous room with a tunnel

        #center coordinates of previous room
        (prev_x, prev_y) = rooms[num_rooms-1].center()

        #draw a coin (random number that is either 0 or 1)
        if libtcod.random_get_int(0, 0, 1) == 1:
          #first move horizontally, then vertically
          self.create_h_tunnel(prev_x, new_x, prev_y)
          self.create_v_tunnel(prev_y, new_y, new_x)
        else:
          #first move vertically, then horizontally
          self.create_v_tunnel(prev_y, new_y, prev_x)
          self.create_h_tunnel(prev_x, new_x, new_y)

      #finally, append the new room to the list
      rooms.append(new_room)
      num_rooms += 1

  def draw(self,con):
    #go through all tiles, and set their background color according to the FOV
    for y in range(self.height):
      for x in range(self.width):
        visible = libtcod.map_is_in_fov(self.fov_map, x, y)
        libtcod.console_set_char_background(con, x, y, self.map[x][y].get_colour(visible), libtcod.BKGND_SET)

  def is_blocked(self,x,y):
    return self.map[x][y].blocked

  def is_pos_visible(self,x,y):
    return libtcod.map_is_in_fov(self.fov_map, x, y)

  def recompute_fov(self,x,y):
    libtcod.map_compute_fov(self.fov_map, x, y, self.torch_radius,self.fov_light_walls, self.fov_algo)

  def unblock_tile(self, tile):
    tile.blocked = False
    tile.block_sight = False

  def create_room(self, room):
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
      for y in range(room.y1 + 1, room.y2):
        self.unblock_tile(self.map[x][y])

  def create_h_tunnel(self,x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
      self.unblock_tile(self.map[x][y])

  def create_v_tunnel(self,y1, y2, x):
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
      self.unblock_tile(self.map[x][y])
