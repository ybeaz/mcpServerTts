from typing import TypedDict, Union, Any, Dict, List, Tuple


def isDictKey(dictIn: dict, key: Union[str, int]) -> bool:
  ''' Description: Function to check if there is a key in dict
    Import: from shared.isDictKey import isDictKey
  '''

  try:
    return (dictIn[key] == None
            or dictIn[key] == 0
            or dictIn[key]) \
      and True
  except KeyError:
    return False
