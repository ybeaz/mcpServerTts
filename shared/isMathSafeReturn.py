from typing import TypedDict, Union, Any, Dict, List, Tuple

from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT
# For debugging: EXIT(comment('EXIT'))

# class KwargsType(TypedDict):
#   prop: float or int

KwargsType = {
  'prop': Dict
}

kwargsDefault = {'prop': 1}


def isMathSafeReturn(
  entity: Any,
  operatorName: str,
  entity2: Any = 0,
  defaultValue: Any = 0, **kwargs) -> Any:
  ''' Function to return 0 if one of the input for the operation is not valis for division 
    Parameters:
      numerator: Any,
      denominator: Any,
    **kwargs: info N/A
    Return: str, means something else
    Import: from shared.isMathSafeReturn import isMathSafeReturn
    Test: python -m shared.isMathSafeReturn
          Not implemented yet: python -m shared.__tests__.isMathSafeReturnTest
  '''

  kwargs = {**kwargsDefault, **kwargs}

  try:
    if (isinstance(entity, float) or isinstance(entity, int)):
      if (isinstance(entity2, float) or isinstance(entity2, int)):

        if operatorName == '+':
          return entity + entity2
        elif operatorName == '-':
          return entity - entity2
        elif operatorName == '*':
          return entity * entity2
        elif operatorName == '/':
          return entity / entity2
        elif operatorName == 'abs':
          return abs(entity)
        elif operatorName == '=' or operatorName == 'number' or operatorName == 'substitute':
          return entity2
        else:
          return defaultValue
      else:
        if operatorName == 'abs':
          return abs(entity)
        elif operatorName == '=' or operatorName == 'number' or operatorName == 'substitute':
          return entity2
        else:
          return defaultValue
    elif entity == None or isinstance(entity, str):
      if operatorName == 'concat' or operatorName == 'concatenate':
        return ''.join([str(entity), str(entity2)])
      elif operatorName == '=' or operatorName == 'number' or operatorName == 'substitute':
        return entity2

    return defaultValue

  except Exception as e:
    return defaultValue


if __name__ == "__main__":
  import numpy as np

  #
  ''' -------------------------------------------------------------------------------------
    Should output a proper value '''

  input = [
      {'entity': None, 'operatorName': '=', 'entity2': None, 'expected': None},
      {'entity': 'const', 'operatorName': '=', 'entity2': 3, 'expected': 3},
      {'entity': None, 'operatorName': '=', 'entity2': 2, 'expected': 2},
      {'entity': 3, 'operatorName': '=', 'entity2': 2, 'expected': 2},
      {'entity': 10, 'operatorName': '=', 'entity2': 2, 'expected': 2},
      {'entity': -10, 'operatorName': '=', 'entity2': 0, 'expected': 0},
      {'entity': 0, 'operatorName': '=', 'entity2': 0, 'expected': 0},
      {'entity': 'string', 'operatorName': '=',
       'entity2': 'str2', 'expected': 'str2'},
      {'entity': 10, 'operatorName': '=',
       'entity2': 'string', 'expected': 'string'},

      {'entity': None, 'operatorName': 'number', 'entity2': None, 'expected': None},
      {'entity': 'const', 'operatorName': 'number', 'entity2': 3, 'expected': 3},
      {'entity': None, 'operatorName': 'number', 'entity2': 2, 'expected': 2},
      {'entity': 3, 'operatorName': 'number', 'entity2': 2, 'expected': 2},
      {'entity': 10, 'operatorName': 'number', 'entity2': 2, 'expected': 2},
      {'entity': -10, 'operatorName': 'number', 'entity2': 0, 'expected': 0},
      {'entity': 0, 'operatorName': 'number', 'entity2': 0, 'expected': 0},
      {'entity': 'string', 'operatorName': 'abs', 'entity2': 0, 'expected': 0},
      {'entity': 10, 'operatorName': 'number',
       'entity2': 'string', 'expected': 'string'},

      {'entity': None, 'operatorName': 'abs', 'entity2': None, 'expected': 0},
      {'entity': 3, 'operatorName': 'abs', 'entity2': None, 'expected': 3},
      {'entity': None, 'operatorName': 'abs', 'entity2': 2, 'expected': 0},
      {'entity': 3, 'operatorName': 'abs', 'entity2': 2, 'expected': 3},
      {'entity': 10, 'operatorName': 'abs', 'entity2': 2, 'expected': 10},
      {'entity': -10, 'operatorName': 'abs', 'entity2': 0, 'expected': 10},
      {'entity': 0, 'operatorName': 'abs', 'entity2': 0, 'expected': 0},
      {'entity': 'string', 'operatorName': 'abs', 'entity2': 0, 'expected': 0},
      {'entity': 10, 'operatorName': 'abs', 'entity2': 'string', 'expected': 10},

      {'entity': None, 'operatorName': '+', 'entity2': None, 'expected': 0},
      {'entity': 3, 'operatorName': '+', 'entity2': None, 'expected': 0},
      {'entity': None, 'operatorName': '+', 'entity2': 2, 'expected': 0},
      {'entity': 3, 'operatorName': '+', 'entity2': 2, 'expected': 5},
      {'entity': 10, 'operatorName': '+', 'entity2': 2, 'expected': 12},
      {'entity': 10, 'operatorName': '+', 'entity2': 0, 'expected': 10},
      {'entity': 0, 'operatorName': '+', 'entity2': 0, 'expected': 0},
      {'entity': 'string', 'operatorName': '+', 'entity2': 0, 'expected': 0},
      {'entity': 10, 'operatorName': '+', 'entity2': 'string', 'expected': 0},

      {'entity': None, 'operatorName': '-', 'entity2': None, 'expected': 0},
      {'entity': 3, 'operatorName': '-', 'entity2': None, 'expected': 0},
      {'entity': None, 'operatorName': '-', 'entity2': 2, 'expected': 0},
      {'entity': 3, 'operatorName': '-', 'entity2': 2, 'expected': 1},
      {'entity': 10, 'operatorName': '-', 'entity2': 2, 'expected': 8},
      {'entity': 10, 'operatorName': '-', 'entity2': 0, 'expected': 10},
      {'entity': 0, 'operatorName': '-', 'entity2': 0, 'expected': 0},
      {'entity': 'string', 'operatorName': '-', 'entity2': 0, 'expected': 0},
      {'entity': 10, 'operatorName': '-', 'entity2': 'string', 'expected': 0},

      {'entity': None, 'operatorName': '*', 'entity2': None, 'expected': 0},
      {'entity': 3, 'operatorName': '*', 'entity2': None, 'expected': 0},
      {'entity': None, 'operatorName': '*', 'entity2': 2, 'expected': 0},
      {'entity': 3, 'operatorName': '*', 'entity2': 2, 'expected': 6},
      {'entity': 10, 'operatorName': '*', 'entity2': 2, 'expected': 20},
      {'entity': 10, 'operatorName': '*', 'entity2': 0, 'expected': 0},
      {'entity': 0, 'operatorName': '*', 'entity2': 0, 'expected': 0},
      {'entity': 'string', 'operatorName': '*', 'entity2': 0, 'expected': 0},
      {'entity': 10, 'operatorName': '*', 'entity2': 'string', 'expected': 0},

      {'entity': None, 'operatorName': '/', 'entity2': None, 'expected': 0},
      {'entity': 3, 'operatorName': '/', 'entity2': None, 'expected': 0},
      {'entity': None, 'operatorName': '/', 'entity2': 2, 'expected': 0},
      {'entity': 3, 'operatorName': '/', 'entity2': 2, 'expected': 1.5},
      {'entity': 10, 'operatorName': '/', 'entity2': 2, 'expected': 5},
      {'entity': 10, 'operatorName': '/', 'entity2': 0, 'expected': 0},
      {'entity': 0, 'operatorName': '/', 'entity2': 0, 'expected': 0},
      {'entity': 'string', 'operatorName': '/', 'entity2': 0, 'expected': 0},
      {'entity': 10, 'operatorName': '/', 'entity2': 'string', 'expected': 0},
  ]

  for item in input:
    entity = item['entity']
    entity2 = item['entity2']
    operatorName = item['operatorName']
    expected = item['expected']

    outputed = isMathSafeReturn(entity, operatorName, entity2)

    # PRINTP({'item': item, 'outputed': outputed,
    #        'expected': expected}, comment(),
    #        #  **{'exit': True}
    #        )

    np.testing.assert_equal(np.asanyarray(outputed, dtype=object),
                            np.asanyarray(expected, dtype=object),
                            verbose=True)

  print('\n\n------------------------------------------ Test SUCCESS ------------------------------------------\n\n')
