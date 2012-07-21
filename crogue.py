import sys
sys.path.append(sys.path[0] + "/libtcod-1.5.0/")
import libtcodpy as libtcod
from gobject import GObject
from map import Map

class Game(object):

	def __init__(self, font):
		self.screen_height = 50
		self.screen_width = 80
		self.font = sys.path[0] + '/libtcod-1.5.0/data/fonts/' + font		
		self.map = Map(80,45)
		self.fov_recompute = True
		#create the root console
		libtcod.console_set_custom_font(self.font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
		libtcod.console_init_root(self.screen_width, self.screen_height, 'crogue', False)
		#Create a console to draw to the screen
		self.con = libtcod.console_new(self.screen_width, self.screen_height)

		self.player = GObject(self.map.starting_pos[0], self.map.starting_pos[1], '@', libtcod.white)		
		self.objects = [self.player]

		#TODO: Abstract this to a game class

	def handle_keys(self):
		key = libtcod.console_wait_for_keypress(True)
		if key.vk == libtcod.KEY_ENTER and key.lalt:
			#Alt+Enter: toggle fullscreen
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
		elif key.vk == libtcod.KEY_ESCAPE:
			return True  #exit game

		#movement keys
		if libtcod.console_is_key_pressed(libtcod.KEY_UP):
			self.move_player(0,-1)
		elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
			self.move_player(0,1)
		elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
			self.move_player(-1,0)
		elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
			self.move_player(1,0)

	def move_player(self, x, y):
		self.player.move(self.map,x,y)
		self.fov_recompute = True

	def render_all(self):
			for object in self.objects:
				object.draw(self.con, self.map)
			if self.fov_recompute:
				#recompute FOV if needed (the player moved or something)
				self.fov_recompute = False
				self.map.recompute_fov(self.player.x, self.player.y)
			self.map.draw(self.con)
			libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)

	def main_loop(self):
		while not libtcod.console_is_window_closed():
			libtcod.console_set_foreground_color(self.con, libtcod.white)
			self.render_all()
			
			libtcod.console_flush()    

			for object in self.objects:
				object.clear(self.con)

			exit = self.handle_keys()
			
			if exit:
				break		


g = Game('arial10x10.png')
g.main_loop()



