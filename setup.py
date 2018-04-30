#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import cologne_phonetics

setup(name="cologne_phonetics",
      version=cologne_phonetics.__version__,
      description="Python implementation of the cologne-phonetics algorithm.",
      long_description=cologne_phonetics.__doc__,
      url="https://github.com/provinzkraut/cologne_phonetics",
      author="Janek Nouvertné",
      author_email="j.a.nouvertne@posteo.de",
      license=cologne_phonetics.__license__,
      classifiers=[
                    'Development Status :: 5 - Production/Stable',
                    'License :: OSI Approved :: MIT License',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Education',
                    'Intended Audience :: Other Audience',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Topic :: Text Processing :: Linguistic',
                    'Natural Language :: English',
    ],
    keywords="cologne-phonetics phonetic",
    python_requires=">=3",
    py_modules=["cologne_phonetics"],
    scripts=["cologne_phonetics.py"]
)
