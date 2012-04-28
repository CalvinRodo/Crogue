import libtcodpy as libtcod

class Map(object):
	def __init__(self,width, height):
		self.height = height
		self.width = width		

		self.color_dark_wall = libtcod.Color(0, 0, 100)
		self.color_light_wall = libtcod.Color(130, 110, 150)
		self.color_dark_ground = libtcod.Color(50, 50, 150)
		self.color_light_ground = libtcod.Color(200, 180, 50)

		self.room_max_size = 10
		self.room_min_size = 6
		self.max_rooms = 30
		self.fov_algo = 0  #default FOV algorithm
		self.fov_light_walls = True
		self.torch_radius = 10
		self.starting_pos = self.make_map()	
		self.fov_map = self.make_fovmap()

		

	def make_fovmap(self):
		fov_map = libtcod.map_new(self.width, self.height)
		for y in range(self.height):
			for x in range(self.width):
				libtcod.map_set_properties(fov_map, x, y, not self.map[x][y].block_sight, not self.map[x][y].blocked)
		return fov_map

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
			failed = False
			for other_room in rooms:
				if new_room.intersect(other_room):
					failed = True
					break
			if not failed:
				#this means there are no intersections, so this room is valid

				#"paint" it to the map's tiles
				self.create_room(new_room)

				#center coordinates of new room, will be useful later
				(new_x, new_y) = new_room.center()

				if num_rooms == 0:
					#this is the first room, where the player starts at
					playerx = new_x
					playery = new_y
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
		return [playerx,playery]



	def draw(self,con):
		#go through all tiles, and set their background color according to the FOV
		for y in range(self.height):
			for x in range(self.width):
				visible = libtcod.map_is_in_fov(self.fov_map, x, y)
				wall = self.map[x][y].block_sight
				if not visible:
					#it's out of the player's FOV
					if wall: 
						libtcod.console_set_back(con, x, y, self.color_dark_wall, libtcod.BKGND_SET)
					else:
						libtcod.console_set_back(con, x, y, self.color_dark_ground, libtcod.BKGND_SET)
				else:
					#it's visible
					if wall:
						libtcod.console_set_back(con, x, y, self.color_light_wall, libtcod.BKGND_SET )
					else:
						libtcod.console_set_back(con, x, y, self.color_light_ground, libtcod.BKGND_SET )

	def is_blocked(self,x,y):
		return self.map[x][y].blocked

	def is_pos_visible(self,x,y):
		return libtcod.map_is_in_fov(self.fov_map, x, y)

	def recompute_fov(self,x,y):
		libtcod.map_compute_fov(self.fov_map, x, y, self.torch_radius,self.fov_light_walls, self.fov_algo)

	def create_room(self, room):
		#go through the tiles in the rectangle and make them passable
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.map[x][y].blocked = False
				self.map[x][y].block_sight = False

	def create_h_tunnel(self,x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.map[x][y].blocked = False
			self.map[x][y].block_sight = False

	def create_v_tunnel(self,y1, y2, x):
		#vertical tunnel
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.map[x][y].blocked = False
			self.map[x][y].block_sight = False

class Tile(object):
	#a tile of the map and its properties
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked

		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked

		self.block_sight = block_sight

class Rect(object):
	def __init__(self,x,y,w,h):
		self.x1 = x
		self.y1 = y 
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)

	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and 
				self.y1 <= other.y2 and self.y2 >= other.y1)