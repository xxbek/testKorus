import argparse
from typing import Iterator
import logging


logging.basicConfig(level=logging.INFO)


def _get_int_from_file(path: str) -> Iterator[int]:
    """Outputs numbers sequentially from a file"""
    with open(path, 'r') as f:
        for row in f:
            row = row.strip()
            try:
                if row.isnumeric() or row.lstrip('-').isnumeric():
                    yield int(row)
            except ValueError:
                logging.warning(f'Error by getting value {row}')


def _find_subsequence_len(path: str) -> str:
    """Find max len subsequence in file"""
    subsequence_len, current_len = 0, 0
    for value in _get_int_from_file(path):
        if value > 0:
            current_len += 1
        else:
            current_len = 0

        if current_len > subsequence_len:
            subsequence_len = current_len

    return 'max_length\n' + str(subsequence_len)


def _main() -> None:
    args = _parse_args()
    input_path = args.input_data
    result = _find_subsequence_len(input_path)
    logging.info(result)


def _parse_args() -> argparse.Namespace:
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Tool to generate test logs.')

    parser.add_argument(
        'input_data',
        metavar='<INPUT DATA>',
        type=str,
        help='path to file with data',
    )

    return parser.parse_args()


if __name__ == '__main__':
    _main()

