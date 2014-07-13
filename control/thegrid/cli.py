"""
cli.py

Really simple command line interface to the HTTP API.
"""

import sys
import requests

import settings


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: {} <command> <value>")
        return

    cmd = sys.argv[1]
    try:
        val = sys.argv[2]
    except IndexError:
        val = None
    port, password = settings.API_PORT, settings.API_PASSWORD
    url = "http://localhost:{}/command".format(port)
    data = {"cmd": cmd, "val": val}
    r = requests.post(url, auth=("cli", password), data=data)
    print(r)
    print(r.text)


if __name__ == "__main__":
    main()
