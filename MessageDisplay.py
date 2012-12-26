from di import DI

__author__ = 'calvin'
import libtcodpy as libtcod
import textwrap

#TODO: Add ability for colors to message list
class MessageDisplay(object):
  _messageList = []
  _maxWidth = 30
  _maxHeight = 13
  _actualWidth = _maxWidth - 2
  _actualHeight = _maxHeight - 2
  _innerPanel = libtcod.console_new(_actualWidth, _actualHeight)
  _console = libtcod.console_new(_maxWidth, _maxHeight)
  _box_created = False

  def __init__(self):
    if MessageDisplay._box_created:
      return

    MessageDisplay._box_created = True

    di = DI()
    gui = di.Request("Gui")
    gui.draw_box(MessageDisplay._console, 0, 0, MessageDisplay._maxWidth, MessageDisplay._maxHeight)

  def render(self):
    index = 0
    buffer = []
    numMessages = (MessageDisplay._actualHeight - 1) * -1
    #Format the messages and add them to the buffer
    for msg in MessageDisplay._messageList[numMessages:]:
      if len(msg) > MessageDisplay._actualWidth:
        buffer.extend(textwrap.wrap(msg, MessageDisplay._actualWidth))
        continue
      buffer.append(msg)

    libtcod.console_rect(MessageDisplay._innerPanel,0,0,MessageDisplay._actualWidth, MessageDisplay._actualWidth,True)
    libtcod.console_set_default_foreground(MessageDisplay._innerPanel, libtcod.white)

    for msg in buffer[numMessages:]:
      libtcod.console_print(MessageDisplay._innerPanel, 2, index, msg.encode())
      index += 1

    libtcod.console_blit(MessageDisplay._innerPanel,0,0,0,0, MessageDisplay._console,1,1)
    return MessageDisplay._console

  def add_message(self, param):
    MessageDisplay._messageList.append(param)