=================
Cologne-phonetics
=================

Cologne-phonetics is a phonetic algorithm similar to Soundex, developed by Hans Postel.
Contrary to Soundex, it's designed specific for the german language.

It involves three steps:

- Generate a code by representing every letter from left to right with a digit, according to a conversion table
- Remove double digits
- Remove every occurence of '0', except as a leading digit

The module itself is quite simple and consists only of the `encode()` function, it's
convinience wrapper `encode_many()` and a simple command line interface.


=========
Usage
=========

.. rubric:: Example: Encoding a string

.. code-block:: python

  >>> import cologne_phonetics
  >>> cologne_phonetics.encode("hello")
  >>> '05'

.. rubric:: Example: Encoding a list of strings

.. code-block:: python

  >>> import cologne_phonetics
  >>> cologne_phonetics.encode_many(["hello", "world"])
  >>> ['05', '3752']

Note that this will return the same result as

.. code-block:: python

>>> cologne_phonetics.encode("hello world")
>>> ['05', '3752']

because substrings seperated by whitespace are encoded as multiple single strings.


Command line interface
======================

.. code-block:: bash

  $ cologne_phonetics.py hello
  05
  $ cologne_phonetics.py hello world
  ['05', '3752']
