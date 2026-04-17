from typing import TypedDict, Union, Any, Dict, List, Tuple

import sys
import pprint
import datetime

from shared.isNumber import isNumber
from shared.isInteger import isInteger
from shared.isIterable import isIterable
from shared.isDictKey import isDictKey
from shared.getDeletedPropValDict import getDeletedPropValDict

# Important: is is used for reimport
from shared.getDebugLine import getDebugLine as comment
# Important: is is used for reimport
from shared.getItExited import getItExited as EXIT


def getItPrinted(obj, commentIn, **kwargs) -> None:
  """ Description: Function to print lists
    Parameters:
      obj: obj to print
      commentIn: to tract PRINT string in the terminal vs code
    **kwargs:
      edgeItems: number of array items in summary at beginning and end of each dimension (default 3)
        see analogy: https://numpy.org/doc/stable/reference/generated/numpy.set_printoptions.html
      parts: top, bottom or both (by default)
      exProps: [] list of object properties to delete
      width: number or 'max' - width of the string in the terminal
      decim: precision of numbers in the list
      maxDecim: 
      count: boolean, default True, count things in the list and print order number in the left column
      maxFormat: max number for "main" formatting
      # checkPoint: number of the check pint by the order in the targeted function
    Import: from shared.getItPrinted import getItPrinted as PRINT
    Testing: python -m shared.getItPrinted
    Links:
      https://stackoverflow.com/a/44356856/4791116
      PrettyPrinter library https://docs.python.org/3/library/pprint.html
  """
  kwargsDefault = {
      'edgeItems': 3,  # options: 'infinite'
      'parts': 'both',
      'exProps': [],
      'width': 128,
      'decim': 6,
      'maxFormat': 1,
      'maxDecim': 2,
      'count': True,
      'isCovertingFloat': True,
      'isNowStr': False,
      'printBefore': '\n',
      'printAfter': '',
      'exit': False
  }
  kwargs = {**kwargsDefault, **kwargs}
  edgeItems = kwargs['edgeItems']
  parts = kwargs['parts']
  exProps = kwargs['exProps']
  width = kwargs['width']
  decim = kwargs['decim']
  maxFormat = kwargs['maxFormat']
  maxDecim = kwargs['maxDecim']
  count = kwargs['count']
  isCovertingFloat = kwargs['isCovertingFloat']
  isNowStr = kwargs['isNowStr']
  printBefore = kwargs['printBefore']
  printAfter = kwargs['printAfter']
  exit = kwargs['exit']

  printedMid = False
  listToPrintMiddle = '... ... ...'

  def printWithConditions(row, i, count, linewidth, decim, maxFormat, maxDecim,
                          obj):
    pp = pprint.PrettyPrinter(compact=True,
                              stream=None,
                              indent=1,
                              width=linewidth,
                              depth=10)
    rowNext = getFormattedVarToDecim(row,
                                     decim,
                                     maxFormat=maxFormat,
                                     maxDecim=maxDecim,
                                     isCovertingFloat=isCovertingFloat)
    if count == True and (type(obj) == tuple
                          or type(obj) == list) and len(obj) > 3:
      if type(rowNext) == str or type(rowNext) == bool or isNumber(rowNext):
        pp.pprint((i, rowNext))
      elif isinstance(rowNext, List) == True or isinstance(rowNext, Tuple) == True:
        rowNext = list(rowNext)  # type: ignore
        pp.pprint([i, *rowNext])
      else:    # type(rowNext) == tuple or type(rowNext) == dict or etc.
        pp.pprint((i, rowNext))
    else:
      pp.pprint(rowNext)

  nowStr = ''
  if isNowStr == True:
    now = datetime.datetime.now()
    nowStr = ' 🕒 ' + now.strftime("%Y-%m-%d %H:%M:%S")

  print(printBefore)
  lineTitle = ''.join((commentIn, nowStr, '  ▷ ', str(type(obj))))
  print(lineTitle)    # 'params', kwargs

  linewidth = sys.maxsize if width == 'max' or width == 'maxsize' else width

  if isinstance(obj, str) or isNumber(obj) or type(obj) == bool:
    print(obj)
  elif isinstance(obj, dict):
    objNext = dict(obj)
    if isDictKey(kwargs, 'exProps') and len(exProps) > 0:
      for exProp in exProps:
        objNext = getDeletedPropValDict(objNext, exProp)
    pp = pprint.PrettyPrinter(stream=None,
                              indent=1,
                              width=linewidth,
                              depth=None)
    pp.pprint(objNext)
  elif isIterable(obj):

    for i, row in enumerate(obj):
      if isInteger(edgeItems):
        if i < edgeItems and (parts == 'both' or parts == 'top'):
          printWithConditions(row, i, count, linewidth, decim, maxFormat,
                              maxDecim, obj)
        elif printedMid == False and i >= edgeItems and i < len(obj) - edgeItems:
          printedMid = True
          print(listToPrintMiddle)
        elif i >= len(obj) - edgeItems and (parts == 'both'
                                            or parts == 'bottom'):
          printWithConditions(row, i, count, linewidth, decim, maxFormat,
                              maxDecim, obj)
      else:
        if count == True:
          print(i, row)
        else:
          print(''.join((str(row), ',')))
  else:
    print('Raw print', obj)

  print(printAfter)

  if exit == True:
    EXIT()


PRINTP = getItPrinted


def getFormattedVarToDecim(entityIn, digits: int = 6, **kwargs):
  """ Description: Funciton to round dict components to a particular number of decimals
    Import: from shared.getFormattedVarToDecim import getFormattedVarToDecim
    Kwargs:
      maxFormat: max number for "main" formatting
      maxDecim: max decim to format "outside" main formatting
      isCovertingFloat: to persist to convert numbers to float or not
  """

  output = []
  if isinstance(entityIn, dict):
    output = {}
    for key in entityIn:
      output[key] = getFormattedVarToDecim(
        entityIn[key], digits, **kwargs)  # type: ignore
  elif isinstance(entityIn, list) or isinstance(entityIn, tuple):
    output = []
    for item in entityIn:
      # type: ignore
      output += [getFormattedVarToDecim(item, digits, **kwargs)]
  else:
    output = entityIn
    # This function does not work: getFormattedVarToDecim(entityIn, digits, **kwargs)  # type: ignore

  return output


class FormatPrinter(pprint.PrettyPrinter):
  """ Description: Custorm formatter to pprint.PrettyPrinter
    Kwargs:
      format: format schema, example
        formats={float: "%.2f", int: "%i", str: '%s'}
    Link: https://stackoverflow.com/a/44356856/4791116
    Example:
      fp = FormatPrinter(
        compact=True, stream=None, indent=1, width=80, depth=10,
        formats=formats, maxFormat=maxFormat
      )
      fp.pformat(anyStr).replace('\n', '').replace('\t', '')
      or / and
      fp.pprint(anyStr)
  """

  def __init__(self, **kwargs):
    keysToOmit = ('formats', 'maxFormat')
    kwargsNext = {key: kwargs[key] for key in kwargs if not key in keysToOmit}
    super().__init__(**kwargsNext)
    self.formats = kwargs['formats']
    self.maxFormat = kwargs['maxFormat']

  def format(self, obj, context, maxlevel, level):
    if type(obj) in self.formats:
      if type(obj) == float and obj > self.maxFormat:
        formatStr = '%.2f'
      else:
        formatStr = self.formats[type(obj)]
      return formatStr % obj, 1, 0
    return pprint.PrettyPrinter.format(self, obj, context, maxlevel, level)
