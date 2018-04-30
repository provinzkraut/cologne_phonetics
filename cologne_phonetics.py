#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cologne_phonetics is a Python implementation of the cologne-phonetics, a phonetic
algorithm similar to soundex but optimized for the german language

Documentation can be found at https://github.com/provinzkraut/cologne_phonetics

An online version and API are available at https://phonetics.provinzkraut.de

A detailed explanation of the cologne phonetics can be found at:
https://en.wikipedia.org/wiki/Cologne_phonetics
"""

__author__ = "Janek Nouvertné"
__version__ = "1.2.3"
__license__ = "MIT"

import sys
import re
from collections import Iterable
from argparse import ArgumentParser, ArgumentTypeError


RGX_SPECIAL_CHARS = re.compile(r"[äüößéèáàç]")

RGX_SPECIAL_CHAR_REPLACEMENTS = [
  (re.compile(r"ä"), "ae"),
  (re.compile(r"ö"), "oe"),
  (re.compile(r"ü"), "ue"),
  (re.compile(r"ß"), "s"),
  (re.compile(r"é"), "e"),
  (re.compile(r"è"), "e"),
  (re.compile(r"á"), "a"),
  (re.compile(r"à"), "a"),
  (re.compile(r"ç"), "c"),
]

RGX_RULES = [
        # ignore special characters that have not been replaced at this point
        (re.compile(r"[^a-z]"),         ''),

        ## d,t replacements
        # not before c,s,z
        (re.compile(r"[dt](?![csz])"), '2'),
        # before c,s,z
        (re.compile(r"[dt](?=[csz])"), '8'),

        ### x replacements
        # not after c,k,q
        (re.compile(r"(?<![ckq])x"),   '48'),
        # after c,k,q. insert new x for later comparison. will be removed later
        (re.compile(r"(?<=[ckq])x"),   'x8'),


        ## c replacements
        # at the start before a,h,k,l,o,q,r,u,x
        # | not after s,z before a,h,k,o,q,u,x
        (re.compile(r"^c(?=[ahkloqrux])|(?<![sz])c(?=[ahkoqux])"),   "4"),
        # not before a,h,k,o,q,u,x
        # | not before s,z
        # | at the start, not before a,h,k,l,o,q,r,u,x
        (re.compile(r"c(?![ahkoqux])|(?<=[sz])c|^c(?![ahkloqrux])"), "8"),

        # p not before h
        (re.compile(r"p(?!h)|b"),       '1'),
        # p before h and f,v,w
        (re.compile(r"p(?=h)|[fvw]"),   '3'),
        (re.compile(r"[hx]"),            ""),
        (re.compile(r"[aeijouy]"),      '0'),
        (re.compile(r"[gkq]"),          '4'),
        (re.compile(r"l"),              '5'),
        (re.compile(r"[mn]"),           '6'),
        (re.compile(r"r"),              '7'),
        (re.compile(r"[sz]"),           '8'),

        # repeating digits
        (re.compile(r"(\d)(?=\1)"),     ''),
        (re.compile(r"\B0"),            '')
    ]


def encode(data, concat=False):
    """
    :param data str: Input to be encoded. Every whitespace character will be\
    interpreted as a wordbreak.
    :param concat bool: The intended behaviour of the cologne-phonetics\
    is to ignore special characters. This leads to concatenation for strings\
    with hyphens. If :attr:`concatenate` is set to True` strings connected by\
    hyphens will be treated as two single strings.

    :rtype: dict
    :return: Return a dict of input / encoded substring pairs

    :note: Contrary to many other implementations, in the final pass only\
    repeated **digits** are removed, not repeated **numbers**. Resulting e.g.\
    in ``xx`` being encoded as `4848` and not `48``.
    """

    def _replace_by_rules(rules, s):
        for rule in rules:
            s = rule[0].sub(rule[1], s)
        return s

    def _enc(s):
        s = s.lower()
        if RGX_SPECIAL_CHARS.search(s):
            s = _replace_by_rules(RGX_SPECIAL_CHAR_REPLACEMENTS, s)
        o = s
        s = _replace_by_rules(RGX_RULES, s)
        return o, s


    if not concat:
        data = data.replace("-", " ")
    if " " in data:
        data = data.split(" ")
        result = []
        for i in data:
            result.append(_enc(i))
    else:
        result = [_enc(data)]

    return result


def compare(*data, concat=False):
    """
    Encode and compare strings.

    :param *data: Data to compare. Either at last 2 positional arguments or an iterable
    :param concat bool: Passed to `encode()`

    :returns: True or False

    :raises: ValueError if only one input string is given.
    """

    if not isinstance(data[0], str) and (data[0], Iterable) and len(data) == 1:
        data = data[0]

    if len(data) == 1:
        raise ValueError('Compare called with only one value: "%s"' % data[0])

    last = None
    for s in data:
        res = [r[1] for r in encode(s)]
        if last and res != last:
            return False
        else:
            last = res
    else:
        return True


def cli():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("data",
                        help="string to be encoded")
    parser.add_argument("-c", "--concat",
                        action="store_true",
                        help="treat words connected by hyphens as seperate words")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="show detailed information")
    parser.add_argument("-p", "--pretty",
                       action="store_true",
                       help="use in combination with --verbose to format output nicely")
    args = parser.parse_args()
    res = encode(args.data, concat=args.concat)
    if args.verbose:
        sep = '\n' if args.pretty else ', '
        out = sep.join([r[0]+": "+r[1] for r in res])
    else:
        out = ', '.join([r[1] for r in res])
    print(out)

if __name__ == "__main__": # pragma: no cover
    cli()
