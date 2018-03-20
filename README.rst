.. _stable: https://raw.githubusercontent.com/provinzkraut/cologne_phonetics/1.0.2/cologne_phonetics.py
.. _unstable: https://raw.githubusercontent.com/provinzkraut/cologne_phonetics/master/cologne_phonetics.py

=================
Cologne-phonetics
=================

Cologne-phonetics is a phonetic algorithm similar to Soundex, wich encodes words into a phonetic code, making it possible to compare how they *sound* rather than how they're *written*.
It was developed by Hans Postel and contrary to Soundex, it's designed specific for the german language.

It involves three steps:

- Generate a code by representing every letter from left to right with a digit, according to a conversion table
- Remove double digits
- Remove every occurence of '0', except as a leading digit

The module itself is quite simple and consists only of the `encode()` function, it's
convinience wrapper `encode_many()` and a simple command line interface.

========
Install
========

cologne_phonetics is available on PyPi for Python 3.4+. So it can be installed it via pip:

.. code-block:: bash

  pip install cologne_phonetics

Alternively, cou can download the latest unstable_ or release_ directly.

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


Command line interface
======================

.. code-block:: bash

  $ cologne_phonetics.py hello
  05
  $ cologne_phonetics.py hello world
  ['05', '3752']


===================
Special characters
===================

Most special characters are simply ignored, but even within the set of special characters,
there are some that are even *more* special.
Special characters are all characters that are not ascii-characters between A and Z.


Word breaks and hyphens
========================

By default, words connected by hyphens, e.g. ``meier-lüdenscheid``, are treated
as a single word. So ``meier-lüdenscheid`` would become ``6752682``. If you
want it to be treated as two seperate words, you can pass a ``concat=False``
to the encode functions. In this case, a list with the seperated, encoded words
will be returned.

While at first this doesn't seem to make a difference in the result, other than it being split
into a list of strings, in some cases it can make a difference.

.. code-block:: python

  >>> cologne_phonetics.encode("weiss-chemie")
  >>> ['38', '46']
  >>> cologne_phonetics.encode("weiss-chemie", concat=False)
  >>> '386'

As you can see, a ``4`` got lost here.
In the case that you *really* want to compare the connected words you may use this option,
but in general there's not much use to it.


Umlaut and special character replacement
=========================================

Umlaute and some other special charactersare converted to their non-special equivalent.

======  ==========
Umlaut  conversion
======  ==========
ü       ue
ö       oe
ä       ae
ß       s
é       e
è       e
á       a
à       a
======  ==========
