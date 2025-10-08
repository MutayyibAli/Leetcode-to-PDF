import src.helper as helper
from src.state import State
from src.printHelper import PrintHelper
import sys
import os
import time
import re
import colorama
from joblib import Memory
import requests
import json
from types import SimpleNamespace
from bs4 import BeautifulSoup
import weasyprint
from google import genai


# Initialize joblib memory for caching
memory = Memory(".cache", verbose=0)


@memory.cache
def fetch_question(slug):
    questionGQL = open("assets/graphql/question.gql").read()

    base = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": questionGQL,
    }

    result = requests.get("https://leetcode.com/graphql", json=base)
    time.sleep(1)  # To avoid hitting rate limits
    return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))


@memory.cache
def fetch_solutions(slug, languageTags):
    solutionGQL = open("assets/graphql/solution.gql").read()

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

    result = requests.get("https://leetcode.com/graphql", json=base)
    time.sleep(1)  # To avoid hitting rate limits
    return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))


@memory.cache
def fetch_post(postId):
    postGQL = open("assets/graphql/post.gql").read()

    base = {
        "operationName": "getPost",
        "variables": {"postId": postId},
        "query": postGQL,
    }

    result = requests.get("https://leetcode.com/graphql", json=base)
    time.sleep(1)  # To avoid hitting rate limits
    return json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d))


def fetch_ai_response(prompt):
    try:
        PrintHelper.print_info("Generating AI explanation (may take a while)...")
        client = genai.Client(api_key="AIzaSyBTFBZ22rrSD5yWBYqkwRmAGyp6aWUr--4")
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        PrintHelper.clear_last_lines(1)
    except Exception:
        PrintHelper.clear_last_lines(1)
        return False

    return response.text


def cache_ai_explanation(question):
    if question not in State.cached_sol:
        cache_solution(question)

    prompt = (
        "Do not say 'here is' at the beginning or at the end, only provide the output as markdown.\n"
        + "You are an expert programmer and educator. Given a coding problem and solutions, your task is to provide a clear solutions.\n"
        + "Output Format: (Follow exactly)\n"
        + "List of all the approaches to solution(First 'Brute Force Approach' then all other approaches in the solution below (from worst to best))\n"
        + "For each approach, give a brief step by step explanation of the approach (with time & space complexity in the last sentence) and code snippet in C++\n"
        + "Lastly provide pythonic solution for best approach only\n"
        + "\n\nHTML of problem from Leetcode:\n"
        + open(
            f"leetcode_cache/questions/{question}.html", "r", encoding="utf-8"
        ).read()
        + "\n\nSolutions:\n"
        + open(
            f"leetcode_cache/solutions/{question}.html", "r", encoding="utf-8"
        ).read()
    )

    response = fetch_ai_response(prompt)
    explanation = helper.markdown_to_html(response)

    # Prepare ai explanation HTML
    htmlStr = "<div class='ai-explanation'>"
    htmlStr += explanation
    htmlStr += "</div>"

    # Save solution HTML
    with open(f"leetcode_cache/ai/{question}.html", "w", encoding="utf-8") as f:
        f.write(htmlStr)

    return True


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
        if postIdPy != postIdCpp:
            votePy = solutionDataPy[0].post.voteCount
            postPy = fetch_post(postIdPy).data.post.content
    except SimpleNamespace:
        return False

    def process_post(post):
        # Decode unicode escape sequences
        post = bytes(post, "utf-8").decode("unicode_escape")
        post = post.encode("utf-8", errors="ignore").decode("utf-8")

        # Remove images, headers, and horizontal lines
        post = re.sub(r"!\[.*?\]\(.*?\)", "", post)
        post = (
            post.replace("# ", "#### ")
            .replace("\n---\n", "")
            .replace("---\n", "")
            .replace("C++", "cpp")
        )
        post = re.sub(r"^(```[^`\n]+)\s\[\]\s*$", r"\1", post, flags=re.MULTILINE)

        return post

    # Process and Save Post Content
    solutionC = process_post(postCpp)

    if postIdPy != postIdCpp:
        solutionPy = process_post(postPy)
        posts = (
            "# Cpp Solution:\n"
            + solutionC
            + "\n\n\n"
            + "# Python Solution:\n"
            + solutionPy
        )
    else:
        posts = "# Solution:\n" + solutionC

    with open(f"leetcode_cache/posts/{question}.md", "w", encoding="utf-8") as f:
        f.write(posts)

    solutionC = helper.markdown_to_html(solutionC)

    # Prepare solution HTML
    htmlStr = "<div class='cpp-solution'>"
    htmlStr += f"<h4>{solutionDataCpp[0].title} [Votes: {voteCpp}]</h4>"
    htmlStr += solutionC
    htmlStr += "</div>"

    if postIdPy != postIdCpp:
        solutionPy = helper.markdown_to_html(solutionPy)

        htmlStr += "<div class='python-solution'>"
        htmlStr += f"<h4>{solutionDataPy[0].title} [Votes: {votePy}]</h4>"
        htmlStr += solutionPy
        htmlStr += "</div>"

    # Save solution HTML
    with open(f"leetcode_cache/solutions/{question}.html", "w", encoding="utf-8") as f:
        f.write(htmlStr)

    return True


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


def cache_question(question):
    try:
        questionData = fetch_question(question).data.question
    except SimpleNamespace:
        return False

    # Remove all empty lines
    questionData.content = questionData.content.replace("<p>&nbsp;</p>", "")

    # Prepare question HTML
    htmlStr = "<div>"
    htmlStr += f"<h2 class='question-title'>{questionData.title}</h2>"

    # Add question metadata
    htmlStr += "<p>"
    htmlStr += f"<strong>Leetcode No: </strong><a href='https://leetcode.com/problems/{question}'>{questionData.questionFrontendId}</a>"
    htmlStr += " | "
    htmlStr += f"<strong>Difficulty: </strong>{questionData.difficulty}"
    if questionData.topicTags:
        htmlStr += " | "
        tags = ", ".join([topic.name for topic in questionData.topicTags])
        htmlStr += f"<strong>Tags:</strong> {tags}"
    htmlStr += "</p>"
    htmlStr += questionData.content
    if questionData.hints:
        htmlStr += "<p><strong>Hints:</strong></p>"
        htmlStr += "<ul class='hints'>"
        for hint in questionData.hints:
            htmlStr += f"<li>{hint}</li>"
        htmlStr += "</ul>"
    htmlStr += "</div>"

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


def make_pdf(option):
    PrintHelper.print_info("Generating HTML...")

    # Prepare HTML
    contentStr = "<h3 style='text-align: center;'>List of Questions</h3>"
    htmlStr = ""
    totalQ = 0
    qCount = 0
    headingCount = 0

    for idx, question in enumerate(State.lines):
        # Skip invalid lines
        if not State.is_question(question) and not State.is_heading(question):
            continue

        # Headings
        if State.is_heading(question):
            headingCount += 1
            qCount = 0
            heading = question[2:].strip()

            if headingCount > 1:
                contentStr += "</ol>"
            contentStr += (
                "<p style='font-weight:bold;'>"
                + str(chr(64 + headingCount))
                + ". "
                + str(heading)
                + "</p>"
            )

            htmlStr += f"<h2>{chr(64 + headingCount)}. {heading}</h2>"
            contentStr += '<ol style="column-count: 2;">'
            print(heading)
            continue

        # Question
        qTitle = ""
        if State.is_question(question):
            question = question[len("https://leetcode.com/problems/") :].split("/")[0]

            PrintHelper.print_info(f"Processing: {question}")

            # Question Statement
            if "q" in option and question in State.all_cached_questions:
                try:
                    qHtml = open(
                        f"leetcode_cache/questions/{question}.html",
                        "r",
                        encoding="utf-8",
                    ).read()
                    qCount += 1

                    soup = BeautifulSoup(qHtml, "html.parser")
                    # Extract text from first h2 tag
                    qTitle = soup.find("h2").get_text(strip=True)

                    qHtml = (
                        "<div><h2 class='question-title'>"
                        + str(qCount)
                        + ". "
                        + qHtml[len("<div><h2 class='question-title'>") :]
                    )

                    contentStr += "<li>" + qTitle + "</li>"
                    htmlStr += qHtml
                    htmlStr += '<div style="page-break-before: always;"></div>'

                except FileNotFoundError:
                    PrintHelper.clear_last_lines(1)
                    PrintHelper.print_error(f"Question not found: {question}")
                    continue
            else:
                qCount += 1
                contentStr += "<li>" + qTitle + "</li>"
                htmlStr += "<h2>" + str(qCount) + ". " + qTitle + "</h2>"

            totalQ += 1

            # Solution
            if "s" in option and question in State.all_cached_sol:
                try:
                    sHtml = open(
                        f"leetcode_cache/solutions/{question}.html",
                        "r",
                        encoding="utf-8",
                    ).read()
                    htmlStr += f'<h2 style="text-align: center;">{qCount}. {qTitle} -- Community Solution</h2>'
                    htmlStr += sHtml
                    htmlStr += '<div style="page-break-before: always;"></div>'
                except FileNotFoundError:
                    PrintHelper.print_error(f"Solution not found: {question}")

            # AI Explanation
            if "ai" in option and question in State.all_cached_ai:
                try:
                    aiHtml = open(
                        f"leetcode_cache/ai/{question}.html", "r", encoding="utf-8"
                    ).read()
                    htmlStr += f'<h2 style="text-align: center;">{qCount}. {qTitle} -- AI Explanation</h2>'
                    htmlStr += aiHtml
                    htmlStr += '<div style="page-break-before: always;"></div>'
                except FileNotFoundError:
                    PrintHelper.print_error(f"AI Explanation not found: {question}")

            PrintHelper.clear_last_lines(1)

    PrintHelper.print_success(f"Processed {totalQ} questions.")

    # Wrap with HTML and CSS
    styles = open("assets/styles.css").read()

    htmlStr, css = helper.highlight_code_blocks(htmlStr)

    finalHtml = "<html><head><meta charset='utf-8'><style>"
    finalHtml += styles
    finalHtml += css
    finalHtml += "</style></head><body>"
    finalHtml += f"<div>{contentStr}</div>"
    finalHtml += '<div style="page-break-before: always;"></div>'
    finalHtml += htmlStr
    finalHtml += "</body></html>"

    # Generate PDF
    PrintHelper.print_info("Generating PDF...")
    pdf = weasyprint.HTML(string=finalHtml).write_pdf()

    # Save PDF
    filename = f"leetcode-{State.file_name}.pdf"
    with open(filename, "wb") as f:
        f.write(pdf)

    PrintHelper.print_success(f"PDF generated successfully: {filename}")


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
        PrintHelper.clear_last_lines(1)
        while True:
            sel = PrintHelper.print_options(
                "Select PDF Type:",
                [
                    "Questions Only",
                    "Solutions Only",
                    "AI Explanations Only",
                    "Questions + Solutions",
                    "Questions + AI Explanations",
                    "Questions + Solutions + AI Explanations",
                    "Back",
                ],
            )
            content = []
            match sel:
                case "Questions Only":
                    content.append("q")
                case "Solutions Only":
                    content.append("s")
                case "AI Explanations Only":
                    content.append("ai")
                case "Questions + Solutions":
                    content.append("q")
                    content.append("s")
                case "Questions + AI Explanations":
                    content.append("q")
                    content.append("ai")
                case "Questions + Solutions + AI Explanations":
                    content.append("q")
                    content.append("s")
                    content.append("ai")
                case "Back":
                    break

            make_pdf(content)

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
                    helper.clear_folder("leetcode_cache/posts")
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
