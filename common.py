"""Shared helpers for the My-Shodan-Scripts collection.

Every script imports get_api_key() from here, so the Shodan API key lives in
one place: the SHODAN_API_KEY environment variable. Nothing needs editing in
the scripts themselves.

    export SHODAN_API_KEY=your-key-here
    python3 docker/docker.py
"""

import os
import sys


def get_api_key():
    """Return the Shodan API key from the SHODAN_API_KEY environment variable.

    Exits with a clear message when the variable is not set, instead of
    failing later with an opaque Shodan API error.
    """
    key = os.environ.get("SHODAN_API_KEY")
    if not key:
        sys.exit(
            "error: set the SHODAN_API_KEY environment variable, e.g.\n"
            "  export SHODAN_API_KEY=your-key-here"
        )
    return key


def open_output(path, mode="a"):
    """Open an output file for appending, creating parent directories as needed.

    Replaces bare open() calls so scripts no longer fail when cfg/ or
    cfg-hijacked/ does not exist yet.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    return open(path, mode)
