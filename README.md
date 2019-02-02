# Implement robust-to-missing-characters Base64 decoding with the standard 64 place-values: A-Z; a-z; 0-9; +; /.

## N.B. This is only robust in the sense that the method will return a decoded string and not throw an un-caught exception in any case of missing characters; the missing characters in the input data mean those returned data may have little relation to the data that were originally encoded

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
