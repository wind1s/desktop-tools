#!/usr/bin/env python3

from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(
        "Validate",
        description="Takes URL, IPv4, IPv6, Email address, Phone number (s) and validates them.",
    )
    add_arg = parser.add_argument

    add_arg("-e", "--encoding")
