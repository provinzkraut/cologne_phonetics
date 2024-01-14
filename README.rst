.. _`PyPi`: https://pypi.org/project/cologne-phonetics/


=================
Cologne-phonetics
=================


.. image:: https://img.shields.io/pypi/pyversions/cologne-phonetics.svg
    :alt: PyPI version


Contents
========

- `Cologne-phonetics`_

  - `Introduction`_
  - `Examples`_
- `Installation`_
- `Usage`_

  - `Module contents`_

    - `encode`_
    - `compare`_
  - `Examples`_
  - `Command line interface`_
- `Special characters`_

  - `Word breaks and hyphens`_
  - `Umlaut and special character replacement`_

- `Changelog`_

  - `1.2.0`_
  - `1.2.1`_
  - `1.2.2`_
  - `1.2.3`_
  - `1.2.4`_
  - `1.3.0`_
  - `1.3.1`_
  - `2.0.0`_



Introduction
============

Cologne-phonetics is a phonetic algorithm similar to Soundex, wich encodes words
into a phonetic code, making it possible to compare how they *sound* rather than how they're *written*.
It was developed by Hans Postel and contrary to Soundex, it's designed specific
for the german language.

It involves three steps:

- Generate a code by representing every letter from left to right with a digit, according to a conversion table
- Remove double digits
- Remove every occurrence of '0', except as a leading digit

The module itself is quite simple and consists only of the `encode`_ and `compare`_  functions
and a simple command line interface.


Examples
========

.. code-block:: bash

  $ cologne_phonetics.py "peter pédter"
  127, 127
  $ cologne_phonetics.py "umwelt umhwält"
  06352, 06352
  $ cologne_phonetics.py "urlaub uhrlaup"
  0751, 0751

As you can see, similar sounding names produce the same result, with respect to the *correct* pronunciation.

.. code-block:: bash

  $ cologne_phonetics.py "peter peta"
  127, 12

This does not give the same result for each word because they may *look* similar,
but (when pronounced correctly) don't really *sound* alike.


============
Installation
============

cologne_phonetics runs with Python 3.4+ or PyPy 3.5.
It is available on `PyPi`_ and can be installed it via pip:

.. code-block:: bash

  pip install cologne_phonetics


=====
Usage
=====

Module contents
===============

.. _encode:

encode(data, *concat=False*)
  Return a list of result tuples.

  Each tuple consists of the string that was encoded and its result.

  If the input string is altered in any way before encoding, the tuple will
  contain the altered version.

  .. code-block:: python

    >>> cologne_phonetics.encode("bäteS")
    >>> [('baetes', '128')]

  If ``concat=True`` is passed, words connected with hyphens will be treated as
  a single words.

  Most of the time, the list will be ``len(result_list) == 1``. Only if the input string
  contains a space character or a hyphen it is splitted into substrings and each
  substring will be encoded seperately.

.. _compare:

compare(\*data, *concat=False*)
  Parameter
    \*data. Either at last 2 positional arguments or an iterable
  Returns
    `True` if all encoded strings are equal, else `False`
  Raises
    `ValueError`.
    If only one value is submitted or the submitted Iterable is of lenght 1.


Command line interface
======================

.. code-block:: bash

  $ cologne_phonetics.py hello
  05
  $ cologne_phonetics.py hello world
  05, 3752


Optional arguments
~~~~~~~~~~~~~~~~~~~~

-h, --help
  show this help message and exit
-c, --concat
  treat words connected by hyphens as seperate words
-v, --verbose
  show detailed information
-p, --pretty
  format output nicely



===================
Special characters
===================

Special characters are all characters that are not ascii-characters between A and Z.
Most special characters are simply ignored, but even within the set of special characters,
there are some that are even *more* special.


Word breaks and hyphens
========================

By default, words connected by hyphens, e.g. ``meier-lüdenscheid`` are seperated.
So ``meier-lüdenscheid`` would become ``'67', '52682'``. If you
want it to be treated as a single word, you can pass a ``concat=True``
to the encode functions.

While at first this doesn't seem to make a difference in the result, other than it being split
into a list of strings, in some cases it can make a difference.

.. code-block:: python

  >>> cologne_phonetics.encode("weiss-chemie")
  >>> [('weiss', '38'), ('chemie', '46')]
  >>> cologne_phonetics.encode("weiss-chemie", concat=True)
  >>> [('weiss-chemie', '386')]

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


=========
Changelog
=========

1.2.0
=====

- Removed `encode_many()`
- `encode()` now allways returns a list of result tuples
- Added `--verbose` and `--pretty` options to CLI
- New function: `compare()`

1.2.1
=====

- Fixed an error that would lead to case sensitive comparison in `compare`_

1.2.2
=====

- Another error in `compare`_ was found (and fixed); Compare didn't actually compare output. It compared input. This was due to bad tests and introduced in 1.2.0, with the change that made `encode`_ always return a tuple as a result

1.2.3
=====

- PyPy 3.5 is now officially supported
- A bug was fixed that would lead `encode`_ to sometimes an preprocessed rather than the altered string in the result tuple


1.2.4
=====

- Drop support for Python 3.4 and 3.5
- Add tests for Python 3.8 and 3.9
- Remove deprecated ``Iterable`` import. See #1


1.3.0
=====

- Add more robust replacement of diacritic using ``unicodedata`` (provided by `Tobias Bengfort <https://github.com/xi>`_ )
- Add type hints
- Fix issue where ``concat`` parameter of `compare`_ wasn't passed to `encode`_


1.3.1
=====

- Run tests against Python 3.10
- Add missing Readme to pyproject.toml
- Drop Python 3.6 support


2.0.0
=====

- Drop Python 3.7 support
- Test against Python 3.11 and 3.12
