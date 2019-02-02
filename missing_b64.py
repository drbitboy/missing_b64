"""
Implement robust-to-missing-characters Base64 decoding with the standard
64 place-values: A-Z; a-z; 0-9; +; /.

Method missing_b64.b64decode(...) is wrappper for base64.b64decode

Application:  Python 3; may work in Python 2.7 as-is or with fiddling

Usage in scripts:

  from missing_base64 import b64decode
  decoded_data = b64decode(ascii_string)
  decoded_data = b64decode(ascii_bytes)

Testing (BASH shown):  

  [DEBUG=] python missing_base64.py

  Expected output:

    {'tries': 260, 'successes': 260, 'failures': 0}


References:

1) https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding

2) https://en.wikipedia.org/wiki/Base64https://en.wikipedia.org/wiki/Base64

"""
import os
import sys
import base64

########################################################################
### For testing
do_debug = 'DEBUG' in os.environ


########################################################################
class MISSING_B64_NOT_ASCII(Exception):
  """Exception for non-ASCII inputs"""
  pass


########################################################################
def b64decode(arg):
  """
  Wrapper for base64.b64decode
  - Expects Base64 encoded ASCII data as input argument arg
  - Returns decoded data as bytes object
  - Expects arg uses standard Base64 place-values:  A-Z; a-z; 0-9; +; /.
  - Robust to missing Base64 encoded characters
    - Will not return original data in this case
  - Not necessarily robust to corrupted characters in arg
  - Throws MISSING_B64_NOT_ASCII exception if arg contains non-ASCII
    characters; implemented via bytes.decode and/or str.encode

  """
  try:
    ### Ensure argument is either bytes ASCII or str ASCII
    if isinstance(arg,bytes): arg_string = arg.decode('ASCII')
    elif isinstance(arg,str): arg_string = arg.encode().decode('ASCII')
    else                    : assert False
  except:
    raise MISSING_B64_NOT_ASCII('Method missing_b64.b64decode Base64 encoded argument is neither ASCII bytes nor ASCII str')

  try:
    ### Remove any = chars, and try padding with two =s
    ### - This will work with (len(arg') % 4) of 0, 2 or 3
    ###   - arg' is arg with all non-Base64-standard-place-values removed
    return base64.b64decode(arg_string.replace('=','')+'==')

  except base64.binascii.Error as e:
    ### If that failed, padd with A==
    ### - This will work with (len(arg') % 4) of 1
    return base64.b64decode(arg_string.replace('=','')+'A==')

  except:
    ### Execution should never get here
    raise


########################################################################
def test_one(arg,expect_exception=False):
  """
  Test harness, exception-handler+wrapper for missing_b64.b64decode(...)
  - arg:  input argument for missinf_b64.b64decode
  - expect_exception:  True if exception is expected; False if not.

  Return vaoue (3-tuple):
  0:  'OK' if exception expectation was met, else 'FAIL'
  1:  Return value from missing_b64.b64decode if no exception, else None
  2:  None if no exceptions, else the exception

  """
  try:
    rtn = b64decode(arg)
    return (expect_exception and 'FAIL' or 'OK',rtn,None,)
  except Exception as e:
    return (expect_exception and 'OK' or 'FAIL',None,e,)


########################################################################
if "__main__" == __name__:

  ### Initialize success and failure counters
  tries,successes,failures = 0,0,0

  ### Arguments expected to generate exceptions:
  ### - str and True:  non-ASCII strings
  ### - Non-ASCII string object
  ### - Non-ASCII bytes object
  for test_arg in (str
                  ,True
                  ,''.join([chr(i) for i in range(129)])
                  ,''.join([chr(i) for i in range(129)]).encode('LATIN1')
                  ,):

    ### Increment tries, call wraapper
    tries += 1
    status,val,xept = tup = test_one(test_arg,True)

    ### Increment counters.  N.B. OK here means expected exception seen
    if tup[0]=='OK': successes += 1
    else           : failures += 1

    ### Debug output: write argument on one line, 3-tuple on next line
    if do_debug:
      sys.stdout.write('{}:\n  '.format(str((test_arg,))))
      print(tup)

  ### Arguments expected to generate no exceptions
  ### ASCII string objects
  ### ASCII bytes objects
  for test_arg in (''.join([chr(i) for i in range(128)])
                  ,''.join([chr(i) for i in range(128)]).encode('LATIN1')
                  ,):

    ### Start with length of 128, loop over all possible positve lengths
    while test_arg:

      ### Increment tries, call wraapper
      tries += 1
      tup = test_one(test_arg,False)

      ### Increment counters
      if tup[0]=='OK': successes += 1
      else           : failures += 1

      ### Debug output: write argument on one line, 3-tuple on next line
      if do_debug:
        sys.stdout.write('{}:\n  '.format(str((test_arg,))))
        print(tup)

      ### Truncate one character
      test_arg = test_arg[:-1]

  ### Output results
  print(dict(tries=tries,success=successes,failures=failures))

  ### Throw exception if there were any failures
  assert tries and tries==successes and not failures
