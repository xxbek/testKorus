import argparse
import csv
import logging
from typing import TextIO

_RESULT_PATH = 'income_out.csv'

_LOG_PATH = 'log'

logging.basicConfig(
    format='%(asctime)s: %(levelname)s: %(message)s',
    level=logging.INFO,
    filemode='w',
    filename=_LOG_PATH
)


def _get_department(department_path: str) -> list:
    """
    yield ['id', 'start_year', 'end_year', 'name']
    """
    with open(department_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for department in reader:
            yield department


def _check_operation(operation: list, department_id: int) -> bool:
    """
    :param operation: current operation
    :param department_id: current department
    :return: True if operation corresponds department and operation row is correct
    """
    if department_id != int(operation[4]):
        return False

    for value in operation:
        if not value.isdigit():
            logging.warning(f"Input data `{value}` in `{operation}` is not numeric")
            return False

    month = int(operation[2])
    if month < 1 or month > 12:
        logging.warning(f"Month `{month}` is incorrect in input data: `{operation}`")
        return False

    return True


def _count_department_profit(department: list[str], operation_path: str) -> dict:
    """
    Operation written in the form: [id, year, month, day, department_id, income]
    """
    department_id = int(department[0])
    first_year, last_year = int(department[1]), int(department[2])
    profit_counter = {
        year: {month + 1: 0 for month in range(12)} for year in range(first_year, last_year + 1)
    }
    with open(operation_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for operation in reader:
            if _check_operation(operation, department_id):
                year, month, income = map(int, [operation[1], operation[2], operation[5]])
            else:
                continue

            year_profit_counter = profit_counter.get(year)
            if year_profit_counter:
                year_profit_counter[month] += income
            else:
                logging.warning(
                    f"Department `{department[3]}` didn't work in {year}. It worked from {first_year} to {last_year} "
                )

    return profit_counter


def _write_department_profile(department_profit: dict, department_name: str, output: TextIO) -> None:
    for year, month_counter in department_profit.items():
        for month, profit in month_counter.items():
            data = list(map(str, [year, month, department_name, profit]))
            output.write(','.join(data) + '\n')


def _main() -> None:
    args = _parse_args()
    department_path, operation_path = args.operations, args.departments
    output = open(_RESULT_PATH, 'w')
    output.write('year,month,department,income\n')

    for department in _get_department(department_path):
        department_profit = _count_department_profit(department, operation_path)
        _write_department_profile(department_profit, department_name=department[3], output=output)

    output.close()


def _parse_args() -> argparse.Namespace:
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Tool to generate test logs.')

    parser.add_argument(
        'operations',
        metavar='<OPERATIONS>',
        type=str,
        help='path to file with operations data',
    )

    parser.add_argument(
        'departments',
        metavar='<DEPARTMENT>',
        type=str,
        help='path to file with departments data',
    )

    return parser.parse_args()


if __name__ == '__main__':
    _main()

