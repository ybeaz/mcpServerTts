from typing import cast, TypedDict, Union, Any, Dict, List, Tuple

from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT
# For debugging: EXIT(comment('EXIT'))

from shared.isInListRange import isInListRange
from shared.isDictKey import isDictKey


def isEntityKeyRead(dictIn: Union[Dict, List, Tuple, str], keysIn: Union[str, int, Tuple, List], defaultValue: Any) -> Any:
  ''' Description: Function to check entity (Dict, List, Tuple) if there is a key(s) in dict or return designated value
    Import: from shared.isEntityKeyRead import isEntityKeyRead
    Test: python -m shared.__tests__.isEntityKeyReturnTest
  '''
  keys: Union[Tuple, List]
  if isinstance(keysIn, str) == True or isinstance(keysIn, int) == True:
    keys = [keysIn]
  else:
    keys = cast(List, keysIn)

  keysLenM1 = len(keys) - 1

  branchCurrent = dictIn

  for index, key in enumerate(keys):
    if isinstance(branchCurrent, Dict) == True:

      if isDictKey(branchCurrent, key) and keysLenM1 == index:  # type: ignore
        return branchCurrent[key]  # type: ignore
      elif isDictKey(branchCurrent, key) and keysLenM1 > index:  # type: ignore
        branchCurrent = branchCurrent[key]  # type: ignore
      elif isDictKey(branchCurrent, key) == False:  # type: ignore
        return defaultValue

    elif isinstance(branchCurrent, List) == True and isinstance(key, int) == True:

      if isInListRange(branchCurrent, key) and keysLenM1 == index:
        return branchCurrent[key]  # type: ignore
      elif isInListRange(branchCurrent, key) and keysLenM1 > index:
        branchCurrent = branchCurrent[key]  # type: ignore
      elif isInListRange(branchCurrent, key) == False:
        return defaultValue

    else:
      return defaultValue

  return defaultValue
