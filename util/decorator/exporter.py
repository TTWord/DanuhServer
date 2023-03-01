from flask import jsonify

class RepositoryExporter:
  def __init__(self, func):
    self.func = func
    
  def __get__(self, instance, owner):
    def wrapper(*args, **kwargs):
      data = self.func(instance, *args, **kwargs)
      if (type(data) == list):
        return [d.__dict__ for d in data]
      elif (type(data) == dict):
        return data.__dict__
      else:
        return data
    return wrapper