class DI(object):
  _services = {}

  def Register(self, name, generator):
    if name in DI._services:
      raise Exception("existing exception")

    DI._services[name] = generator

  def Request(self,name):
    return DI._services[name]()


