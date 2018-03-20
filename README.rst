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
  >>> 05

.. rubric:: Example: Encoding a list of strings

.. code-block:: python

  >>> import cologne_phonetics
  >>> cologne_phonetics.encode_many(["hello", "world"])
  >>> ['05', '3752']


Special characters
===================

Word breaks and hyphens
~~~~~~~~~~~~~~~~~~~~~~~~

By default, words connected by hyphens, e.g. ``meier-lüdenscheid``, are treated
as a single word. So ``meier-lüdenscheid`` would become ``6752682``. If you
want it to be treated as to seperate words, you can pass a ``concatenate=True``
to the encode functions. In this case, a list with the seperated, encoded words
will be returned.







Command line interface
======================

.. code-block:: bash

  $ cologne_phonetics.py hello
  05
  $ cologne_phonetics.py hello world
  ['05', '3752']
