import argparse
import six

from .client import Client


def main():
    parser = argparse.ArgumentParser(
        description='Read values from your connected multimeter'
    )
    parser.add_argument('port', nargs=1, type=six.text_type)
    parser.add_argument(
        '--timeout', '-t', type=float, dest='timeout', default=3.0
    )
    parser.add_argument(
        '--retries', '-r', type=int, dest='retries', default=3
    )
    args = parser.parse_args()

    dmm = Client(port=args.port[0], retries=args.retries, timeout=args.timeout)

    while True:
        val = dmm.getMeasurement()
        print val

# main hook
if __name__ == "__main__":
    main()
