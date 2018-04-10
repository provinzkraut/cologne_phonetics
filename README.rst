.. _unstable: https://raw.githubusercontent.com/provinzkraut/cologne_phonetics/master/cologne_phonetics.py
.. _release: https://raw.githubusercontent.com/provinzkraut/cologne_phonetics/1.0.2/cologne_phonetics.py

=================
Cologne-phonetics
=================

Contents
========

- `Cologne-phonetics`_

  - `Introduction`_
  - `Examples`_
- `Installation`_
- `Usage`_

  - `Command line interface`_
- `Special characters`_

  - `Word breaks and hyphens`_
  - `Umlaut and special character replacement`_
  


Introduction
============

Cologne-phonetics is a phonetic algorithm similar to Soundex, wich encodes words into a phonetic code, making it possible to compare how they *sound* rather than how they're *written*.
It was developed by Hans Postel and contrary to Soundex, it's designed specific for the german language.

It involves three steps:

- Generate a code by representing every letter from left to right with a digit, according to a conversion table
- Remove double digits
- Remove every occurence of '0', except as a leading digit

The module itself is quite simple and consists only of the ``encode()`` function, it's
convinience wrapper ``encode_many()``` and a simple command line interface.


Examples
==============

.. code-block:: bash

  $ cologne_phonetics.py "peter pédter"
  ['127', '127']
  $ cologne_phonetics.py "umwelt umhwält"
  ['06352', '06352']
  $ cologne_phonetics.py "urlaub uhrlaup"
  ['0751', '0751']

As you can see, similar sounding names produce the same result, with respect to the *right* pronunciation.

.. code-block:: bash

  $ cologne_phonetics.py "peter peta"
  ['127', '12']

As you can see, this does not give the same result for each name because it may seem similar,
but (when pronounced correctly) don't really *sound* the same.


============
Installation
============

cologne_phonetics is available on PyPi for Python 3.4+. So it can be installed it via pip:

.. code-block:: bash

  pip install cologne_phonetics

Alternively, cou can download the latest unstable_ or release_ directly.


=====
Usage
=====

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

Special characters are all characters that are not ascii-characters between A and Z.
Most special characters are simply ignored, but even within the set of special characters,
there are some that are even *more* special.


Word breaks and hyphens
========================

By default, words connected by hyphens, e.g. ``meier-lüdenscheid`` are seperated.
So ``meier-lüdenscheid`` would become ``['67', '52682']``. If you
want it to be treated as a single word, you can pass a ``concat=True``
to the encode functions. In this case, a list with the seperated, encoded words
will be returned.

While at first this doesn't seem to make a difference in the result, other than it being split
into a list of strings, in some cases it can make a difference.

.. code-block:: python

  >>> cologne_phonetics.encode("weiss-chemie")
  >>> ['38', '46']
  >>> cologne_phonetics.encode("weiss-chemie", concat=True)
  >>> '386'

As you can see, a ``4`` got lost here.
In case you *really* want to compare the concatenated words you may use this option,
but in general there's not much use to it.


Umlaut and special character replacement
=========================================

Umlaute and some other special characters are converted to their non-special equivalent.

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
