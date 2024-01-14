#!/usr/bin/env python3
"""
Cologne_phonetics is a Python implementation of the cologne-phonetics, a phonetic
algorithm similar to soundex but optimized for the german language

Documentation can be found at https://github.com/provinzkraut/cologne_phonetics

A detailed explanation of the cologne phonetics can be found at:
https://en.wikipedia.org/wiki/Cologne_phonetics
"""
from __future__ import annotations

__author__ = "Janek Nouvertné"
__version__ = "2.0.0"
__license__ = "MIT"

import re
import sys
import unicodedata
from argparse import ArgumentParser
from typing import Iterable, Pattern

RGX_SPECIAL_CHARS = re.compile(r"[äüöß]")

RGX_SPECIAL_CHAR_REPLACEMENTS = [
    (re.compile(r"ä"), "ae"),
    (re.compile(r"ö"), "oe"),
    (re.compile(r"ü"), "ue"),
    (re.compile(r"ß"), "s"),
]

RGX_RULES = [
    # ignore special characters that have not been replaced at this point
    (re.compile(r"[^a-z]"), ""),
    # d,t replacements
    # not before c,s,z
    (re.compile(r"[dt](?![csz])"), "2"),
    # before c,s,z
    (re.compile(r"[dt](?=[csz])"), "8"),
    # x replacements
    # not after c,k,q
    (re.compile(r"(?<![ckq])x"), "48"),
    # after c,k,q. insert new x for later comparison. will be removed later
    (re.compile(r"(?<=[ckq])x"), "x8"),
    # c replacements
    # at the start before a,h,k,l,o,q,r,u,x
    # | not after s,z before a,h,k,o,q,u,x
    (re.compile(r"^c(?=[ahkloqrux])|(?<![sz])c(?=[ahkoqux])"), "4"),
    # not before a,h,k,o,q,u,x
    # | not before s,z
    # | at the start, not before a,h,k,l,o,q,r,u,x
    (re.compile(r"c(?![ahkoqux])|(?<=[sz])c|^c(?![ahkloqrux])"), "8"),
    # p not before h
    (re.compile(r"p(?!h)|b"), "1"),
    # p before h and f,v,w
    (re.compile(r"p(?=h)|[fvw]"), "3"),
    (re.compile(r"[hx]"), ""),
    (re.compile(r"[aeijouy]"), "0"),
    (re.compile(r"[gkq]"), "4"),
    (re.compile(r"l"), "5"),
    (re.compile(r"[mn]"), "6"),
    (re.compile(r"r"), "7"),
    (re.compile(r"[sz]"), "8"),
    # repeating digits
    (re.compile(r"(\d)(?=\1)"), ""),
    (re.compile(r"\B0"), ""),
]


def _remove_diacritics(s: str) -> str:
    # https://stackoverflow.com/a/518232
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def _replace_by_rules(rules: list[tuple[Pattern[str], str]], s: str) -> str:
    for rule in rules:
        s = rule[0].sub(rule[1], s)
    return s


def encode(data: str, concat: bool = False) -> list[tuple[str, str]]:
    """
    :param data: Input to be encoded. Whitespace characters will be
        interpreted as a wordbreak
    :param concat: The intended behaviour of the cologne-phonetics
        is to ignore special characters. This leads to concatenation for strings
        with hyphens. If ``concat`` is set to ``True``, hyphenated string will be
        treated as separate words

    :return: Return a list of tuples containing sanitised input / encoded substring
        pairs

    :note: Contrary to many other implementations, in the final pass only
        repeated **digits** are removed, not repeated **numbers**. Resulting e.g.
        in ``xx`` being encoded as `4848` and not `48``
    """

    if not concat:
        data = data.replace("-", " ")
    data = data.lower()

    words_encoded = []
    for word in data.split(" "):
        word_clean = _remove_diacritics(
            _replace_by_rules(RGX_SPECIAL_CHAR_REPLACEMENTS, word)
        )
        word_encoded = _replace_by_rules(RGX_RULES, word_clean)
        words_encoded.append((word_clean, word_encoded))
    return words_encoded


def compare(*data: str, concat: bool = False) -> bool:
    """
    Encode and compare strings.

    :param data: Data to compare. Either at last 2 positional arguments or an iterable
    :param concat: Passed to ``encode()``

    :returns: A boolean, indicating whether all passed data is equal after encoding
    :raises: ValueError if only one input string is given
    """

    if (
        not isinstance(data[0], str)
        and isinstance(data[0], Iterable)
        and len(data) == 1
    ):
        data = data[0]

    if len(data) == 1:
        raise ValueError('Compare called with only one value: "%s"' % data[0])

    last = None
    for s in data:
        res = [r[1] for r in encode(s, concat=concat)]
        if last and res != last:
            return False
        else:
            last = res
    else:
        return True


def cli(args: list[str] | None = None) -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("data", help="string to be encoded")
    parser.add_argument(
        "-c",
        "--concat",
        action="store_true",
        help="treat words connected by hyphens as separate words",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show detailed information"
    )
    parser.add_argument(
        "-p",
        "--pretty",
        action="store_true",
        help="use in combination with --verbose to format output nicely",
    )
    parsed_args = parser.parse_args(args)
    res = encode(parsed_args.data, concat=parsed_args.concat)
    if parsed_args.verbose:
        sep = "\n" if parsed_args.pretty else ", "
        out = sep.join([r[0] + ": " + r[1] for r in res])
    else:
        out = ", ".join([r[1] for r in res])
    print(out)


if __name__ == "__main__":  # pragma: no cover
    cli(sys.argv)
