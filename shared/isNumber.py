import numpy as np


def isNumber(variable):
  """ Description: Function to check if variable is a number
    Import: from shared.isNumber import isNumber
    Example: tf = isNumber(5.678)
  """

  return type(variable) == int or \
    type(variable) == float or \
    type(variable) == np.float32 or \
    type(variable) == np.float64
