import sys

import mantis

def main() -> None:
    if '--version' in sys.argv:
        print(mantis.__version__)
        sys.exit(1)
