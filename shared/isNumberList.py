from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT

from shared.isNumber import isNumber


def isNumberList(listIn):
  """ Description: Function to check if it is a list of only numbers
    Import: from shared.isNumberList import isNumberList
    Testing: python -m shared.isNumberList
    Example: ...
  """

  output = True
  for item in listIn:
    if not isNumber(item):
      output = False
      break

  return output


""" Testing and debugging """
if __name__ == "__main__":
  listIn = [3, 5.44, 44.0, 3, 12345.9876543]
  listIn2 = [3, 5.44, 44.0, None, 12345.9876543]
  listIn3 = ['xS3', 'xS3', 44.0, 3, 12345.9876543]

  # PRINTP(
  #     {
  #         'isNumberList-listIn': isNumberList(listIn),
  #         'isNumberList-listIn2': isNumberList(listIn2),
  #         'isNumberList-listIn3': isNumberList(listIn3),
  #     }, 'isNumberList [30]')
