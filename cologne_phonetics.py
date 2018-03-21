#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cologne_phonetics is a Python implementation of the cologne-phonetics, a phonetic
algorithm similar to soundex but optimized for the german language

Documentation can be found at https://github.com/provinzkraut/cologne_phonetics

A detailed explanation of the cologne phonetics can be found at:
https://en.wikipedia.org/wiki/Cologne_phonetics
"""

__author__ = "Janek Nouvertné"
__version__ = "1.1.0"
__license__ = "MIT"

import sys
import re
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
    :param concatenate bool: The intended behaviour of the cologne-phonetics\
    is to ignore special characters. This leads to concatenation for strings\
    with hyphens. If :attr:`concatenate` is set to True` strings connected by\
    hyphens will be treated as two single strings.

    :rtype: str or list
    :return: Return an encoded string if :attr:`data` is a string. Return\
    a list of encoded substrings if :attr:`data` contains a wordbreak.

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
        s = _replace_by_rules(RGX_RULES, s)
        return s


    if not concat:
        data = data.replace("-", " ")
    if " " in data:
        data = data.split(" ")
        _in_data = data
        result = []
        for i in data:
            result.append(_enc(i))
    else:
        _in_data = data
        result = _enc(data)

    return result


def encode_many(data, concat=True):
    """
    Encode a list of strings

    :arg data list: List of strings

    :rtype: list
    :return: List of encoded strings
    """

    result = []
    for s in data:
        result.append(encode(s, concat=concat))
    return result


if __name__ == "__main__":
# def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("data",
                        help="String to be encoded")
    parser.add_argument("-c", "--concat",
                        action="store_true",
                        help="Treat words connected by hyphens as seperate words")
    args = parser.parse_args()
    if " " in args.data:
        res = encode_many(args.data.split(" "), concat=args.concat)
    else:
        res = encode(args.data, concat=args.concat)
    print(res)
