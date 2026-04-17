from typing import TypedDict, Union, Any, Dict, List, Tuple
import errno
import os
import signal
import functools


from shared.getItPrinted import getItPrinted as PRINT, PRINTP, comment, EXIT
# For debugging: EXIT(comment('EXIT'))


class TimeoutError(Exception):
  pass


def timeout(seconds=2, error_message=os.strerror(errno.ETIME)):
  ''' Function to timeout for long running functions 
  Parameters:
    param1: list, means something
  **kwargs: info N/A
  Return: str, means something else
  Link: https://stackoverflow.com/a/2282656/4791116
  Import: from shared.timeout import timeout
  Test: python -m shared.timeout   Not implemented yet: python -m shared.__tests__.timeoutTest
'''
  def decorator(func):
    def _handle_timeout(signum, frame):
      raise TimeoutError(error_message)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      signal.signal(signal.SIGALRM, _handle_timeout)
      signal.alarm(seconds)
      try:
        result = func(*args, **kwargs)
      finally:
        signal.alarm(0)
      return result

    return wrapper

  return decorator


if __name__ == "__main__":
  import numpy as np

  #
  ''' -------------------------------------------------------------------------------------
    Should output a proper value '''

  input: List = []

  outputed = timeout()
  expected = []

  # PRINTP({
  #     'input': input,
  #     'outputed': outputed,
  #     'expected': expected,
  #     'assert_equal': np.asanyarray(outputed, dtype=object) == np.asanyarray(expected, dtype=object)
  # }, comment(), **{'exit': True})

  assert outputed == expected
  np.testing.assert_array_equal(np.asanyarray(outputed, dtype=object),
                                np.asanyarray(expected, dtype=object),
                                verbose=True)

  print('\n\n------------------------------------------ Test SUCCESS ------------------------------------------\n\n')
