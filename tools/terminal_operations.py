import os
from colorama import Fore, Style


def clear_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_blue(message: str) -> None:
    print(Fore.BLUE + message + Style.RESET_ALL)


def print_magenta(message: str) -> None:
    print(Fore.MAGENTA + message + Style.RESET_ALL)


def print_green(message: str) -> None:
    print(Fore.GREEN + message + Style.RESET_ALL)


def print_yellow(message: str) -> None:
    print(Fore.YELLOW + message + Style.RESET_ALL)


def print_red(message: str) -> None:
    print(Fore.RED + message + Style.RESET_ALL)


def print_cyan(message: str) -> None:
    print(Fore.CYAN + message + Style.RESET_ALL)
