#!/usr/bin/env python3
import re
from sys import argv
from argparse import ArgumentParser
from ipaddress import ip_address, IPv4Address, IPv6Address
from functools import lru_cache

LRU_CACHE_SIZE = 128

# Regex to match URLs.
URL_RE = re.compile(
    r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
)

# Regex which matches international phone numbers, with and without country code. Works best without spaces.
PHONE_RE = re.compile(
    r"((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7}))"
)

# General Email Regex (RFC 5322 Official Standard)
EMAIL_RE = re.compile(
    r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
)


@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_url(string: str) -> bool:
    """
    Validates a string for URL.
    """
    return bool(URL_RE.match(string))


@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_ipv4(string: str) -> bool:
    """
    Validates a string for IPv4.
    """
    try:
        result = ip_address(string)
    except ValueError:
        return False

    return isinstance(result, IPv4Address)


@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_ipv6(string: str) -> bool:
    """
    Validates a string for IPv6.
    """
    try:
        result = ip_address(string)
    except ValueError:
        return False

    return isinstance(result, IPv6Address)


@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_email(string: str) -> bool:
    """
    Validates a string for Email.
    """
    return bool(EMAIL_RE.match(string))


@lru_cache(maxsize=LRU_CACHE_SIZE)
def is_phone_num(string: str) -> bool:
    """
    Validates a string for Phone number.
    """
    return bool(PHONE_RE.match(string.replace(" ", "").replace("\t", "").replace("\r", "")))


@lru_cache(maxsize=LRU_CACHE_SIZE)
def validate(string: str) -> list[str]:
    """
    Validates string for URL, IPv4, IPv6, Email and Phone number.
    Returns a list containing the names of valid items.
    """
    return [
        str_type
        for validator, str_type in (
            (is_url, "url"),
            (is_ipv4, "ipv4"),
            (is_ipv6, "ipv6"),
            (is_email, "email"),
            (is_phone_num, "phone number"),
        )
        if validator(string)
    ]


if __name__ == "__main__":
    parser = ArgumentParser(
        "Validate",
        description="Takes URL, IPv4, IPv6, Email address, Phone number (s) and validates them.",
    )
    add_arg = parser.add_argument

    add_arg("-v", "--verbose", dest="verbose", action="store_true", help="Output more details.")
    add_arg("strings", nargs="+", help="Strings to validate.")

    args = parser.parse_args(argv[1:])

    for string in set(args.strings):
        validated_types = validate(string)

        if validated_types:
            print(f"String: {string}")

            for valid_type in validated_types:
                print(f"\tValid {valid_type}")

        elif args.verbose:
            print(f"String: {string}\n\tNo valid types")
