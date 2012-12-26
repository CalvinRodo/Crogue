from collections import UserList

__author__ = 'calvin'

def exists(self, predicate):
  for obj in self:
    if predicate(obj) == True:
      return True
  return False

UserList.exists = exists
