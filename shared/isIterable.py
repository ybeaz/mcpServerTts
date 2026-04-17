
def isIterable(obj):
  """ Description: Function to check if obj iterable
    Import from shared.isIterable import isIterable
  """
  try:
    obj = iter(obj)
    return True
  except:
    # raise TypeError("obj is not iterable")
    return False
