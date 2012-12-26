__author__ = 'calvin'
import libtcodpy as libtcod
import textwrap

#TODO: Add ability for colors to message list
class MessageDisplay(object):
  _messageList = []
  _maxWidth = 20
  _maxHeight = 10
  _panel = libtcod.console_new(_maxWidth, _maxHeight)

  def render(self):
    index = 0
    buffer = []
    numMessages = (MessageDisplay._maxHeight - 1) * -1
    #Format the messages and add them to the buffer
    for msg in MessageDisplay._messageList[numMessages:]:
      if len(msg) > MessageDisplay._maxWidth:
        buffer.extend(textwrap.wrap(msg, MessageDisplay._maxWidth))
        continue
      buffer.append(msg)

    libtcod.console_rect(MessageDisplay._panel,0,0,MessageDisplay._maxWidth,MessageDisplay._maxHeight,True)
    libtcod.console_set_default_foreground(MessageDisplay._panel, libtcod.white)

    for msg in buffer[numMessages:]:
      libtcod.console_print(MessageDisplay._panel, 0, index, msg.encode())
      index += 1

    return MessageDisplay._panel

  def add_message(self, param):
    MessageDisplay._messageList.append(param)