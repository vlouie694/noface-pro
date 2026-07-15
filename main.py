import json
import logging
import secrets
from time import sleep

import requests

from constants import MAX_PROFILE_NUMBER, MIN_PROFILE_NUMBER
from luhn_algorithm import calculate_luhn_check_digit
from utils import is_valid_number

logging.basicConfig(filename='logs/profile_generator.log', level=logging.INFO)


class ProfileNumberGenerator:

    def __init__(self):
        self.generated_numbers = set()

    def generate_random_profile_number(self) -> int:
        number = secrets.SystemRandom().randint(MIN_PROFILE_NUMBER, MAX_PROFILE_NUMBER)
        check_digit = calculate_luhn_check_digit(number)
        return number if check_digit == 0 else self.generate_random_profile_number()

    def generate_unique_random_profile_number(self) -> int:
        number = self.generate_random_profile_number()
        while number in self.generated_numbers:
            number = self.generate_random_profile_number()
        self.generated_numbers.add(number)
        return number


def log_message(message: str, level: str = "info"):
    logging.log(getattr(logging, level.upper()), message)


def display_progress_bar(iteration, total, bar_length=50):
    progress = float(iteration) / float(total)
    arrow = '=' * int(round(progress * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    print(f'Progress: [{arrow + spaces}] {int(progress * 100)}%')


def audit_generated_profile(number: int):
    with open('logs/audit_log.json', 'a') as f:
        json.dump({'profile_number': number}, f)
        f.write(",\n")


if __name__ == "__main__":
    gen = ProfileNumberGenerator()
    count = 10

    for i in range(1, count + 1):
        try:
            number = gen.generate_unique_random_profile_number()
            log_message(f"Generated: {number}")

            is_valid = is_valid_number(number, calculate_luhn_check_digit)
            if is_valid:
                log_message("Number is valid.")
                audit_generated_profile(number)
            else:
                log_message("Number is not valid.", level="error")

            display_progress_bar(i, count)
            sleep(0.1)
        except Exception as e:
            log_message(str(e), level="error")
