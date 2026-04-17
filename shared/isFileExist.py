from typing import TypedDict, Union, Any, Dict, List, Tuple

import os

from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT

# class KwargsType(TypedDict):
#   prop: float or int

KwargsType = {}

kwargsDefault = {}


def isFileExist(baseDir: str, filePathParts: List[str], **kwargs) -> bool:
  ''' Function to check if the file exists
    Parameters:
      param1: list, means something
    **kwargs: info N/A
    Return: str, means something else
    Import: from shared.isFileExist import isFileExist
    Test: python -m shared.isFileExist OR python -m shared.__tests__.isFileExistTest
  '''

  kwargs = {**kwargsDefault, **kwargs}

  filePath = ''.join([baseDir, *filePathParts])

  output = os.path.isfile(filePath)

  return output


if __name__ == "__main__":
  import numpy as np

  # #
  # ''' -------------------------------------------------------------------------------------
  #   Should output a proper value '''

  # input: List = []

  # outputed = isFileExist(input)
  # expected = []

  # PRINTP({'input': input, 'outputed': outputed, 'expected': expected}, comment())

  # assert outputed == expected
  # np.testing.assert_array_equal(np.asanyarray(outputed, dtype=object),
  #                               np.asanyarray(expected, dtype=object),
  #                               verbose=True)
