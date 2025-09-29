import sys
from colorama import Fore, Back, Style


class PrintHelper:
    @staticmethod
    def print_empty_line():
        print()

    @staticmethod
    def clear_last_lines(n=1):
        for _ in range(n):
            # Move cursor up and clear the line
            sys.stdout.write("\033[F\033[K")

    @staticmethod
    def print_line():
        print(Fore.MAGENTA + Style.BRIGHT + "-" * 80)

    @staticmethod
    def print_heading(message):
        print(Style.BRIGHT + message)

    @staticmethod
    def print_info(message):
        print(message)

    @staticmethod
    def print_success(message):
        print(Fore.BLACK + Back.GREEN + Style.BRIGHT + message + " ")

    @staticmethod
    def print_warning(message):
        print(Fore.BLACK + Back.YELLOW + Style.BRIGHT + message + " ")

    @staticmethod
    def print_error(message):
        print(Fore.BLACK + Back.RED + Style.BRIGHT + message + " ")

    @staticmethod
    def print_options(message, options=["Yes", "No"]):
        PrintHelper.print_info(message)
        for idx, option in enumerate(options, start=1):
            print(
                Fore.CYAN
                + Style.BRIGHT
                + f"{idx}. "
                + Fore.WHITE
                + Style.NORMAL
                + option
            )

        numOptions = len(options)
        is_first_attempt = True
        while True:
            choice = input(
                Fore.CYAN
                + "Make your selection"
                + Style.BRIGHT
                + f" (1-{numOptions}): "
            )
            if choice.isnumeric() and 1 <= int(choice) <= numOptions:
                if not is_first_attempt:
                    PrintHelper.clear_last_lines(1)
                PrintHelper.clear_last_lines(numOptions + 2)
                PrintHelper.print_success(f"{options[int(choice) - 1]}")
                return options[int(choice) - 1]
            else:
                if not is_first_attempt:
                    PrintHelper.clear_last_lines(1)
                is_first_attempt = False
                PrintHelper.clear_last_lines(1)
                PrintHelper.print_error(
                    f"ERROR: Please enter a number between 1 and {numOptions}"
                )

    # Test all above methods
    @staticmethod
    def test_print_helper():
        PrintHelper.print_empty_line()
        PrintHelper.print_line()
        PrintHelper.print_heading("This is a Heading")
        PrintHelper.print_info("This is an info message.")
        PrintHelper.print_success("This is a success message.")
        PrintHelper.print_warning("This is a warning message.")
        PrintHelper.print_error("This is an error message.")
        PrintHelper.print_options(
            "Please select an option:", ["Option 1", "Option 2", "Option 3"]
        )
