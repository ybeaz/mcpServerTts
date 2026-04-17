from typing import TypedDict, Union, Any, Dict, List, Tuple

from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT
# For debugging: EXIT(comment('EXIT'))


def isInListRange(listIn, index):
  """ Description: Function to detect if list index out of range
    Import: from shared.isInListRange import isInListRange
    Test: python -m shared.isInListRange
  """

  try:
    return True if (index == 0 and len(listIn) > 0) or listIn[index] else False
  except:
    return False


if __name__ == "__main__":
  import numpy as np
  from shared.getItPrinted import getItPrinted as PRINT, comment, EXIT
  # For debugging: EXIT(comment('EXIT'))

  #
  ''' -------------------------------------------------------------------------------------
    Should output a proper value '''

  input = [
      0, 7.480484003114, 14.844237555271, 21.976351745163, 28.765532316252,
      35.105836376428, 40.898325601400, 46.052610134162, 50.488259088474,
      54.136055645946, 56.939077161335, 58.853583421389, 59.849699196243,
      59.911880432390, 59.039156812436, 57.245146896582, 54.557845609541,
      51.019187389107, 46.684391813275, 41.621101917196, 35.908328646237,
      29.635217916605, 22.899659523140, 15.806759601805
  ]

  outputed = isInListRange(input, 0)  # type: ignore
  expected = True

  # PRINTP({'input': input, 'outputed': outputed,
  #        'expected': expected}, comment(), **{'exit': True})

  np.testing.assert_equal(np.asanyarray(outputed, dtype=object),
                          np.asanyarray(expected, dtype=object),
                          verbose=True)

  print('\n\n------------------------------------------ Test SUCCESS ------------------------------------------\n\n')
