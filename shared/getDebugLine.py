from typing import Dict
from inspect import currentframe, getouterframes

KwargsType = {
  'level': int, 'sign': str
}

kwargsDefault: Dict = {'level': 1, 'sign': '☝'}


def getDebugLine(comment='', **kwargs):
  """ Description: Function to get name of the file and line number for debugging
    :Parameters:
      comment (str): custom comment insted of automatically generated
    :**kwargs:
      level (int): level of nested fuction from which derive a comment
    Import: from shared.getDebugLine import getDebugLine // import

    Testing python -m shared.getDebugLine
    >>> getDebugLine()
    '☛ <doctest __main__.getDebugLine[0]> [1]'

  """

  kwargs = {**kwargsDefault, **kwargs}
  sign = kwargs['sign']

  if sign == 'ok':
    sign = '✔'

  frameCurrent = currentframe()
  framesOuter = getouterframes(frameCurrent, context=1)

  fileName = ''
  lineNumber = ''

  try:

    fileName = framesOuter[kwargs['level']][1].split('/')[-1]
    lineNumber = ' [' + str(framesOuter[kwargs['level']][2]) + ']'
  finally:
    del framesOuter

  fileNameAndLineList = []
  if comment != '':
    fileNameAndLineList = ['☛ ', fileName,
                           lineNumber, '  ', sign, ' ', comment]
  else:
    fileNameAndLineList = ['☛ ', fileName, lineNumber]

  fileNameAndLine = ' '.join(fileNameAndLineList)
  return fileNameAndLine


if __name__ == "__main__":
  print()

  #
  ''' -------------------------------------------------------------------------------------
    Should output a proper value '''

  input: str = 'my comment'

  outputed = getDebugLine(input, sign='ok')
  expected = 'getDebugLine.py  [60]    ✔   my comment'

  printLine = ' '.join(['input: ', input, ' outputed: ',
                       outputed, ' expected: ', expected])

  print(printLine)
  print()

  # assert outputed == expected

 #
  ''' -------------------------------------------------------------------------------------
    Should output a proper value '''

  input: str = 'my comment'

  outputed = getDebugLine(input)
  expected = 'getDebugLine.py  [60]    ☝   my comment'

  printLine = ' '.join(['input: ', input, ' outputed: ',
                       outputed, ' expected: ', expected])

  print(printLine)
  print()

  # assert outputed == expected

 #
  ''' -------------------------------------------------------------------------------------
    Should output a proper value '''

  input: str = ''

  outputed = getDebugLine()
  expected = '☛  getDebugLine.py  [59]'

  printLine = ' '.join(['input: ', input, ' outputed: ',
                       outputed, ' expected: ', expected])

  print(printLine)
  print()
  # assert outputed == expected
