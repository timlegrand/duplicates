import argparse
import logging

from duplicates.processor import process
from duplicates._version import __version_text__


def _main():
    parser = argparse.ArgumentParser(
        description="Browse a directory tree and search for duplicates.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-e', '--exclude', default="", help="list of coma-separated expressions to exclude")
    parser.add_argument('-v', '--version', action='version', version=__version_text__)
    parser.add_argument('path', nargs='?', default=".", help="path as a start for duplicates search")
    options = parser.parse_args()
    options.exclude = options.exclude.split(",")

    logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)

    print(options)

    dups = process(options, logging.getLogger())

    print("--- Duplicates ---")
    print("\n".join(f"{k}: {sorted(e)}" for k, e in sorted(dups.items()) if e))
