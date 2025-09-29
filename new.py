import src.helper as helper
from src.state import State
from src.printHelper import PrintHelper
import sys
import os
import time
import random
import shutil
import re
import colorama
from colorama import Style, Fore, Back
from joblib import Memory
import requests
import json
from types import SimpleNamespace
import markdown
import mdformat
import weasyprint
from google import genai

endpoint = open("assets/endpoint.txt").read().strip()
questionGQL = open("assets/graphql/question.gql").read()
solutionGQL = open("assets/graphql/solution.gql").read()
postGQL = open("assets/graphql/post.gql").read()
styles = open("assets/styles.css").read()

# Initialize joblib memory for caching
memory = Memory(".cache", verbose=0)


@memory.cache
def fetch_question(slug):
    base = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": questionGQL,
    }

    result = requests.get(endpoint, json=base)
    time.sleep(1)  # To avoid hitting rate limits
    return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))


@memory.cache
def fetch_solutions(slug, languageTags):
    base = {
        "operationName": "solutions",
        "variables": {
            "questionSlug": slug,
            "skip": 0,
            "first": 1,
            "orderBy": "most_votes",
            "languageTags": languageTags,
        },
        "query": solutionGQL,
    }

    result = requests.get(endpoint, json=base)
    time.sleep(1)  # To avoid hitting rate limits
    return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))


@memory.cache
def fetch_post(postId):
    base = {
        "operationName": "getPost",
        "variables": {"postId": postId},
        "query": postGQL,
    }

    result = requests.get(endpoint, json=base)
    time.sleep(1)  # To avoid hitting rate limits
    return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))


"""
# def get_ai_preference():
#     while True:
#         print(
#             Fore.CYAN
#             + Style.BRIGHT
#             + "\nSelect the type of solution you want:\n"
#             + Fore.YELLOW
#             + "1. Community Solution\n"
#             + Fore.MAGENTA
#             + "2. AI Explanation\n"
#         )

#         choice = input(Fore.GREEN + "Enter your choice (1 or 2): ").strip()

#         if choice in ["1", "2"]:
#             solution_type = "Community Solution" if choice == "1" else "AI Explanation"
#             print(
#                 Fore.CYAN
#                 + Style.BRIGHT
#                 + f"You selected: {Fore.YELLOW}{solution_type}\n"
#             )
#             break
#         else:
#             print(Fore.RED + "Please enter '1' or '2'.")

#     return True if solution_type == "AI Explanation" else False
"""


def markdown_to_html(md_text):
    htmlText = mdformat.text(md_text)
    htmlText = markdown.markdown(
        htmlText,
        extensions=["fenced_code", "codehilite", "tables", "nl2br", "sane_lists"],
    )

    # Increase heading levels by 1 (e.g., h1 -> h2) to maintain hierarchy
    htmlText = re.sub(
        r"<h([1-5])>(.*?)</h\1>",
        lambda m: f"<h{str(int(m.group(1)) + 1)}>{m.group(2)}</h{str(int(m.group(1)) + 1)}>",
        htmlText,
    )

    # Remove images to avoid clutter
    htmlText = re.sub(r"<img[^>]*>", "", htmlText)

    return htmlText


def cache_ai_explanation(question):
    if question not in State.cached_sol:
        cache_solution(question)

    prompt = (
        "Do not say 'here is' at the beginning or at the end, only provide the output as markdown.\n"
        + "You are an expert programmer and educator. Given a coding problem and solutions, your task is to provide a clear and concise solution.\n"
        + "Output should be as follows:\n"
        + "Explanation of all the different approaches to solution used in above and give time and space complexity of each approach.\n"
        + "Then provide C++ code for the best solution\n"
        + "Then provide Python code for the best solution\n"
        + "\n\nHTML of problem from Leetcode:\n"
        + open(
            f"leetcode_cache/questions/{question}.html", "r", encoding="utf-8"
        ).read()
        + "\n\nSolution:\n"
        + open(
            f"leetcode_cache/solutions/{question}.html", "r", encoding="utf-8"
        ).read()
    )

    try:
        client = genai.Client(api_key="AIzaSyBTFBZ22rrSD5yWBYqkwRmAGyp6aWUr--4")
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
    except Exception:
        return False

    response = markdown.markdown(response.text)

    # Prepare ai explanation HTML
    htmlStr = "<div class='ai-explanation'>"
    htmlStr += response
    htmlStr += "</div>"
    htmlStr += '<p style="page-break-before: always" ></p>'

    # Save solution HTML
    with open(f"leetcode_cache/ai/{question}.html", "w", encoding="utf-8") as f:
        f.write(htmlStr)

    return True


def cache_solution(question):
    try:
        solutionDataCpp = fetch_solutions(
            question, ["cpp"]
        ).data.questionSolutions.solutions
        solutionDataPy = fetch_solutions(
            question, ["python", "python3"]
        ).data.questionSolutions.solutions
    except SimpleNamespace:
        return False

    try:
        postIdCpp = solutionDataCpp[0].post.id
        voteCpp = solutionDataCpp[0].post.voteCount
        postCpp = fetch_post(postIdCpp).data.post.content

        postIdPy = solutionDataPy[0].post.id
        votePy = solutionDataPy[0].post.voteCount
        postPy = fetch_post(postIdPy).data.post.content
    except SimpleNamespace:
        return False

    def process_post(post):
        # Decode unicode escape sequences
        post = bytes(post, "utf-8").decode("unicode_escape")
        post = post.encode("utf-8", errors="ignore").decode("utf-8")

        # Add language label to code blocks and fix codehilite formatting
        post = (
            re.sub(
                r"^```(\w+)",
                lambda m: f"```{m.group(1)}\nLanguage: {m.group(1)}",
                post,
                flags=re.MULTILINE,
            )
            .replace("```", "``` ")
            .replace("[]", "")
        )

        # Fix relative image paths
        post = post.replace(
            "../Figures", f"https://leetcode.com/problems/{question}/Figures"
        )

        return post

    # Process and Save Post Content
    solutionC = process_post(postCpp)
    solutionPy = process_post(postPy)
    posts = "Cpp Solution:\n" + solutionC + "\n\n\n" + "Python Solution:\n" + solutionPy
    with open(f"leetcode_cache/posts/{question}.html", "w", encoding="utf-8") as f:
        f.write(posts)

    solutionC = markdown_to_html(solutionC)
    solutionPy = markdown_to_html(solutionPy)

    # Prepare solution HTML
    htmlStr = "<div class='cpp-solution'>"
    htmlStr += f"<h2>{solutionDataCpp[0].title} -- Votes: {voteCpp}</h2>"
    htmlStr += solutionC
    htmlStr += "</div>"
    htmlStr += "\n\n\n"
    htmlStr += "<div class='python-solution'>"
    htmlStr += f"<h2>{solutionDataPy[0].title} -- Votes: {votePy}</h2>"
    htmlStr += solutionPy
    htmlStr += "</div>"
    htmlStr += '<p style="page-break-before: always" ></p>'

    # Save solution HTML
    with open(f"leetcode_cache/solutions/{question}.html", "w", encoding="utf-8") as f:
        f.write(htmlStr)

    return True


def cache_question(question):
    try:
        questionData = fetch_question(question).data.question
    except SimpleNamespace:
        return False

    # Prepare question HTML
    htmlStr = "<div>"
    htmlStr += f"<h2><a href='https://leetcode.com/problems/{question}'>[{questionData.questionFrontendId}]</a> {questionData.title}</h2>"
    if questionData.topicTags:
        tags = ", ".join([topic.name for topic in questionData.topicTags])
        htmlStr += f"<strong>{questionData.difficulty}</strong>   Tags: {tags}"
    htmlStr += questionData.content
    if questionData.hints:
        htmlStr += "<h3>Hints</h3>"
        htmlStr += "<ul>"
        for hint in questionData.hints:
            htmlStr += f"<li>{hint}</li>"
        htmlStr += "</ul>"
    htmlStr += "</div>"
    htmlStr += '<p style="page-break-before: always" ></p>'

    # Save question HTML
    with open(f"leetcode_cache/questions/{question}.html", "w", encoding="utf-8") as f:
        f.write(htmlStr)

    return True


def fetch_missing_questions():
    missing_questions = State.missing_questions()
    count = 0
    for idx, question in enumerate(missing_questions):
        PrintHelper.print_success(f"Fetched {count} questions.")
        PrintHelper.print_info(
            f"Fetching {idx + 1} of {len(missing_questions)}: {question}"
        )

        status = cache_question(question)
        PrintHelper.clear_last_lines(2)

        if status:
            count += 1
        else:
            PrintHelper.print_error(f"Failed: {question}")
            continue

    State.update_cached_questions()
    PrintHelper.print_success(
        f"Fetched {count} of {len(missing_questions)} questions successfully."
    )


def fetch_missing_solutions():
    missing_solutions = State.missing_solutions()
    count = 0
    for idx, question in enumerate(missing_solutions):
        PrintHelper.print_success(f"Fetched {count} solutions.")
        PrintHelper.print_info(
            f"Fetching {idx + 1} of {len(missing_solutions)}: {question}"
        )

        status = cache_solution(question)
        PrintHelper.clear_last_lines(2)

        if status:
            count += 1
        else:
            PrintHelper.print_error(f"Failed: {question}")
            continue

    State.update_cached_solutions()
    PrintHelper.print_success(
        f"Fetched {count} of {len(missing_solutions)} solutions successfully."
    )


def fetch_missing_ai_explanations():
    fetch_missing_ai_explanations = State.missing_ai_explanations()
    count = 0
    for idx, question in enumerate(fetch_missing_ai_explanations):
        PrintHelper.print_success(f"Fetched {count} AI explanations.")
        PrintHelper.print_info(
            f"Fetching {idx + 1} of {len(fetch_missing_ai_explanations)}: {question}"
        )

        status = cache_ai_explanation(question)
        PrintHelper.clear_last_lines(2)

        if status:
            count += 1
        else:
            PrintHelper.print_error(f"Failed: {question}")
            continue

    State.update_cached_ai_explanations()
    PrintHelper.print_success(
        f"Fetched {count} of {len(fetch_missing_ai_explanations)} AI explanations successfully."
    )


def select_list():
    files = [f for f in os.listdir("questions_lists") if f.endswith(".txt")]
    selectedFile = PrintHelper.print_options("Select a question list:", files)

    return selectedFile


def initial_setup():
    # Create necessary directories if they don't exist
    if not os.path.exists(".cache"):
        os.makedirs(".cache")
    if not os.path.exists("leetcode_cache"):
        os.makedirs("leetcode_cache")
    if not os.path.exists("leetcode_cache/questions"):
        os.makedirs("leetcode_cache/questions")
    if not os.path.exists("leetcode_cache/solutions"):
        os.makedirs("leetcode_cache/solutions")
    if not os.path.exists("leetcode_cache/posts"):
        os.makedirs("leetcode_cache/posts")
    if not os.path.exists("leetcode_cache/ai"):
        os.makedirs("leetcode_cache/ai")

    # Clean corrupted files
    helper.remove_small_files("leetcode_cache", max_size=100)

    # Read cache state
    State.read_cache()

    # Auto-reset colorama styles after each print
    colorama.init(autoreset=True)


def main():
    initial_setup()

    State.get_lines(select_list())

    def generate_pdf():
        # TODO: Implement PDF generation logic
        pass

    def fetch_new_data():
        PrintHelper.clear_last_lines(1)
        while True:
            sel = PrintHelper.print_options(
                "Select Data:",
                [
                    "Fetch Missing Questions",
                    "Fetch Missing Solutions",
                    "Fetch Missing AI Explanations",
                    "Back",
                ],
            )
            match sel:
                case "Fetch Missing Questions":
                    fetch_missing_questions()
                case "Fetch Missing Solutions":
                    fetch_missing_solutions()
                case "Fetch Missing AI Explanations":
                    fetch_missing_ai_explanations()
                case "Back":
                    break
        PrintHelper.clear_last_lines(1)

    def clear_old_data():
        PrintHelper.clear_last_lines(1)
        while True:
            sel = PrintHelper.print_options(
                "Select Data to Clear:",
                [
                    "Clear Cached Questions",
                    "Clear Cached Solutions",
                    "Clear Cached AI Explanations",
                    "Clear LeetCode Cookies",
                    "Back",
                ],
            )
            match sel:
                case "Clear Cached Questions":
                    helper.clear_folder("leetcode_cache/questions")
                    State.update_cached_questions()
                case "Clear Cached Solutions":
                    helper.clear_folder("leetcode_cache/solutions")
                    State.update_cached_solutions()
                case "Clear Cached AI Explanations":
                    helper.clear_folder("leetcode_cache/ai")
                    State.update_cached_ai_explanations()
                case "Clear LeetCode Cookies":
                    memory.clear(warn=False)
                case "Back":
                    break

        PrintHelper.clear_last_lines(1)

    while True:
        State.print_summary()
        op = PrintHelper.print_options(
            "Select Operation:",
            [
                "Generate PDF",
                "Fetch New Data",
                "Clear Old Data",
                "Exit",
            ],
        )

        match op:
            case "Generate PDF":
                generate_pdf()
            case "Fetch New Data":
                fetch_new_data()
            case "Clear Old Data":
                clear_old_data()
            case "Exit":
                sys.exit(0)


if __name__ == "__main__":
    main()
