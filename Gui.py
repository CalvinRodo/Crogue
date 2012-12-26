__author__ = 'calvin'
import libtcodpy as libtcod

class Gui(object):
  _nwcorner = chr(201)
  _necorner = chr(187)
  _swcorner = chr(200)
  _secorner = chr(188)
  _vert = chr(186)
  _hori = chr(205)

  def draw_box(self, con, x, y, w, h):
    libtcod.console_put_char(con,x,     y,      Gui._nwcorner)
    libtcod.console_put_char(con,x,     h - 1,  Gui._swcorner)
    libtcod.console_put_char(con,w - 1 , y,      Gui._necorner)
    libtcod.console_put_char(con,w  - 1, h - 1  , Gui._secorner)
    self.draw_vert(con,x, y + 1,  h - 2)
    self.draw_vert(con,w - 1, y + 1,  h - 2)
    self.draw_hori(con,x + 1, y ,  w - 2)
    self.draw_hori(con,x + 1, h - 1,  w - 2)


  def draw_vert(self, con, x, y, h):
    libtcod.line_init(x,y,x,h)
    (xc,yc) = (x,y)
    while((xc,yc) != (None,None)):
      libtcod.console_put_char(con,xc,yc,Gui._vert)
      (xc,yc) = libtcod.line_step()

  def draw_hori(self, con, x, y, w):
    libtcod.line_init(x,y,w,y)
    (xc,yc) = (x,y)
    while((xc,yc) != (None,None)):
      libtcod.console_put_char(con,xc,yc,Gui._hori)
      (xc,yc) = libtcod.line_step()

