import os
import sys
from colorama import Fore, Style
from src.printHelper import PrintHelper


class State:
    file_name = ""
    lines = []
    selected_questions = []
    all_cached_questions = []
    all_cached_sol = []
    all_cached_ai = []
    cached_questions = []
    cached_sol = []
    cached_ai = []

    @classmethod
    def get_lines(cls, filepath):
        cls.file_name = filepath[: len(".txt")]
        try:
            file_path = os.path.join("questions_lists", filepath)
            with open(file_path) as f:
                cls.lines = f.read().strip().split("\n")
        except FileNotFoundError:
            PrintHelper.print_error(f"ERROR: {filepath} not found.")
            sys.exit(1)

        # Remove duplicates
        cls.lines = list(dict.fromkeys(cls.lines))

        cls.update_selected_questions()

    @classmethod
    def update_selected_questions(cls):
        for line in cls.lines:
            # Skip empty lines and invalid URLs
            if line == "" or not line.startswith("https://leetcode.com/problems/"):
                continue

            cls.selected_questions.append(
                line[len("https://leetcode.com/problems/") :].split("/")[0]
            )
        cls.read_cache()

    @classmethod
    def update_cached_questions(cls):
        lines = os.listdir("leetcode_cache/questions")
        cls.all_cached_questions = [
            line[:-5] for line in lines if line.endswith(".html")
        ]
        cls.cached_questions = [
            q for q in cls.all_cached_questions if q in cls.selected_questions
        ]

    @classmethod
    def update_cached_solutions(cls):
        lines = os.listdir("leetcode_cache/solutions")
        cls.all_cached_sol = [line[:-5] for line in lines if line.endswith(".html")]
        cls.cached_sol = [q for q in cls.all_cached_sol if q in cls.selected_questions]

    @classmethod
    def update_cached_ai_explanations(cls):
        lines = os.listdir("leetcode_cache/ai")
        cls.all_cached_ai = [line[:-5] for line in lines if line.endswith(".html")]
        cls.cached_ai = [q for q in cls.all_cached_ai if q in cls.selected_questions]

    @classmethod
    def read_cache(cls):
        cls.update_cached_questions()
        cls.update_cached_solutions()
        cls.update_cached_ai_explanations()

    @classmethod
    def missing_questions(cls):
        return [q for q in cls.selected_questions if q not in cls.all_cached_questions]

    @classmethod
    def missing_solutions(cls):
        return [q for q in cls.selected_questions if q not in cls.all_cached_sol]

    @classmethod
    def missing_ai_explanations(cls):
        return [q for q in cls.selected_questions if q not in cls.all_cached_ai]

    @classmethod
    def print_summary(cls):
        PrintHelper.print_line()
        print(
            f"{Style.BRIGHT}{Fore.YELLOW}Selected Questions: {len(cls.selected_questions)}"
        )
        PrintHelper.print_line()
        print(
            f"{Fore.MAGENTA}|{'':^15}|{'Questions':^20}|{'Solutions':^20}|{'AI Explanations':^20}|"
        )
        print(
            f"{Fore.MAGENTA}|{Fore.BLUE}{'Cached':^15}{Fore.MAGENTA}|"
            f"{Fore.BLUE}{len(cls.all_cached_questions):^20}{Fore.MAGENTA}|"
            f"{Fore.BLUE}{len(cls.all_cached_sol):^20}{Fore.MAGENTA}|"
            f"{Fore.BLUE}{len(cls.all_cached_ai):^20}{Fore.MAGENTA}|"
        )
        print(
            f"{Fore.MAGENTA}|{Fore.GREEN}{'Matched':^15}{Fore.MAGENTA}|"
            f"{Fore.GREEN}{len(cls.cached_questions):^20}{Fore.MAGENTA}|"
            f"{Fore.GREEN}{len(cls.cached_sol):^20}{Fore.MAGENTA}|"
            f"{Fore.GREEN}{len(cls.cached_ai):^20}{Fore.MAGENTA}|"
        )
        print(
            f"{Fore.MAGENTA}|{Fore.RED}{'Missing':^15}{Fore.MAGENTA}|"
            f"{Fore.RED}{len(cls.missing_questions()):^20}{Fore.MAGENTA}|"
            f"{Fore.RED}{len(cls.missing_solutions()):^20}{Fore.MAGENTA}|"
            f"{Fore.RED}{len(cls.missing_ai_explanations()):^20}{Fore.MAGENTA}|"
        )
        PrintHelper.print_line()

    @staticmethod
    def is_question(line):
        return line.startswith("https://leetcode.com/problems/") and line != ""

    @staticmethod
    def is_heading(line):
        return line.startswith("* ") and line != ""
