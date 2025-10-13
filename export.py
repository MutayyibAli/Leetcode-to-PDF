import src.helper as helper
from src.state import State
from src.printHelper import PrintHelper
import sys
import os
import time
import ast
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


def fetch_ai_response(prompt, key):
    try:
        PrintHelper.print_info("Generating AI explanation (may take a while)...")
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        PrintHelper.clear_last_lines(1)
    except Exception:
        PrintHelper.clear_last_lines(1)
        return "<ERROR>"

    return response.text


def cache_ai_explanation(question, key):
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

    response = fetch_ai_response(prompt, key)
    if response == "<ERROR>":
        PrintHelper.clear_last_lines(1)
        return False
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

    def get_api_key():
        try:
            with open(".api/keys.txt", "r") as f:
                keys = ast.literal_eval(f.read().strip())

                key = keys[keys["key"].strip()]
        except FileNotFoundError:
            PrintHelper.print_info(
                "Get Gemini API key from https://aistudio.google.com/."
            )
            key = input("Enter Gemini API key: ").strip()
            PrintHelper.clear_last_lines(1)

        try:
            client = genai.Client(api_key=key)
            client.models.generate_content(
                model="gemini-2.5-pro",
                contents="Testing...",
            )
            return key
        except Exception:
            return "<ERROR>"

    key = get_api_key()
    if key == "<ERROR>":
        PrintHelper.print_error("Invalid API key. Please check your key and try again.")
        return
    else:
        PrintHelper.print_info("API key is valid.")

    count = 0
    for idx, question in enumerate(fetch_missing_ai_explanations):
        PrintHelper.print_success(f"Fetched {count} AI explanations.")
        PrintHelper.print_info(
            f"Fetching {idx + 1} of {len(fetch_missing_ai_explanations)}: {question}"
        )

        status = cache_ai_explanation(question, key)
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


def make_pdf(option, data):
    PrintHelper.print_info("Compiling HTML...")

    # Table of Contents
    isFirstHeading = True
    contentsHtml = "<div id='table-of-contents'>"
    for item in range(len(data["table"])):
        if data["headings"][item] is not None:
            if not isFirstHeading:
                contentsHtml += "</div>"
            isFirstHeading = False

            contentsHtml += f"<h3>{data['table'][item]}</h3>"
            contentsHtml += "<hr>"
            contentsHtml += "<div class='two-col'>"
        else:
            contentsHtml += f"<p>{data['table'][item]}</p>"

    contentsHtml += "</div>"

    # Body
    bodyHtml = "<div id='body'>"
    for item in range(len(data["table"])):
        if data["headings"][item] is not None:
            bodyHtml += "<div style='height: 0.5cm;'></div>"
            bodyHtml += f"<h1 class='title'>{data['table'][item]}</h1>"
            continue

        if "q" in option and data["statements"][item] is not None:
            bodyHtml += "<div style='height: 0.5cm;'></div>"
            bodyHtml += "<div class='statement'>"
            bodyHtml += f"<h2 class='title'>{data['table'][item]}</h2>"
            bodyHtml += "<hr>"
            bodyHtml += data["statements"][item]
            bodyHtml += "</div>"
            bodyHtml += '<div style="page-break-before: always;"></div>'

        if "s" in option and data["solutions"][item] is not None:
            bodyHtml += "<div class='solution'>"
            bodyHtml += f"<h2 class='title'>{data['table'][item]} - Solution</h2>"
            bodyHtml += "<hr>"
            bodyHtml += data["solutions"][item]
            bodyHtml += "</div>"
            bodyHtml += '<div style="page-break-before: always;"></div>'

        if "ai" in option and data["ai_explanations"][item] is not None:
            bodyHtml += "<div class='ai-explanation'>"
            bodyHtml += f"<h2 class='title'>{data['table'][item]} - Explanation</h2>"
            bodyHtml += "<hr>"
            bodyHtml += data["ai_explanations"][item]
            bodyHtml += "</div>"
            bodyHtml += '<div style="page-break-before: always;"></div>'

    bodyHtml += "</div>"

    soup = BeautifulSoup(bodyHtml, "html.parser")
    soup.find_all("div")[-1].decompose()
    bodyHtml = str(soup)

    # Wrap with HTML and CSS
    styles = open("assets/styles.css").read()

    bodyHtml, bodyStyles = helper.highlight_code_blocks(bodyHtml)

    finalHtml = "<html><head><meta charset='utf-8'><style>"
    finalHtml += styles
    finalHtml += bodyStyles
    finalHtml += "</style></head><body>"
    finalHtml += "<h1 class='title'>Table of Contents</h1>"
    finalHtml += "<hr>"
    finalHtml += contentsHtml
    finalHtml += '<div style="page-break-before: always;"></div>'
    finalHtml += bodyHtml
    finalHtml += "</body></html>"

    PrintHelper.print_info("Saving HTML...")

    # Generate PDF
    PrintHelper.print_info("Generating PDF...")
    pdf = weasyprint.HTML(string=finalHtml).write_pdf()

    # Save PDF
    if not os.path.exists(".output"):
        os.makedirs(".output")
    filename = f"{State.file_name}_{'_'.join(option)}.pdf"
    with open(os.path.join(".output", filename), "wb") as f:
        f.write(pdf)

    PrintHelper.print_success(f"PDF generated successfully: {filename}")


def process_cached_data():
    steps = len(State.lines)
    table = [None] * steps
    headings = [None] * steps
    questions = [None] * steps
    statements = [None] * steps
    solutions = [None] * steps
    ai_explanations = [None] * steps

    hCount = 1
    qCount = 1
    missing = {"q": 0, "s": 0, "ai": 0}

    def int_to_roman(num):
        val = [50, 40, 10, 9, 5, 4, 1]
        syms = ["L", "XL", "X", "IX", "V", "IV", "I"]
        roman = ""
        for i in range(len(val)):
            count = num // val[i]
            roman += syms[i] * count
            num -= val[i] * count
        return roman

    for idx, line in enumerate(State.lines):
        # Headings
        if State.is_heading(line):
            headings[idx] = line[2:].strip()
            table[idx] = f"{int_to_roman(hCount)}. {headings[idx]}"
            hCount += 1
            continue

        # Question
        line = line[len("https://leetcode.com/problems/") :].split("/")[0]
        PrintHelper.print_info(f"Processing: {line}")
        everythingFound = True

        # Question Statement
        if line in State.all_cached_questions:
            try:
                qHtml = open(
                    f"leetcode_cache/questions/{line}.html",
                    "r",
                    encoding="utf-8",
                ).read()

                # Get question title
                soup = BeautifulSoup(qHtml, "html.parser")
                qTitle = soup.find("h2").get_text(strip=True)

                # Remove question title from statement
                soup.find("h2").decompose()

                soup.find("p").insert_after(soup.new_tag("hr"))

                # Add section breaks
                for p in soup.find_all("p"):
                    text = p.get_text(strip=True)
                    if (
                        text == "Example 1:"
                        or text == "Constraints:"
                        or text == "Hints:"
                        or text == "Custom Judge:"
                    ):
                        p.insert_before(soup.new_tag("hr"))

                questions[idx] = qTitle
                statements[idx] = str(soup)
                table[idx] = f"{qCount}. {qTitle}"

                qCount += 1

            except FileNotFoundError:
                PrintHelper.clear_last_lines(1)
                missing["q"] += 1
                everythingFound = False
                PrintHelper.print_error("Question not found.")

        # Solution
        if line in State.all_cached_sol:
            try:
                sHtml = open(
                    f"leetcode_cache/solutions/{line}.html",
                    "r",
                    encoding="utf-8",
                ).read()
                soup = BeautifulSoup(sHtml, "html.parser")
                [hr.decompose() for hr in soup.find_all("hr")]
                solutions[idx] = str(soup)
            except FileNotFoundError:
                missing["s"] += 1
                everythingFound = False
                PrintHelper.print_error("Solution not found.")

        # AI Explanation
        if line in State.all_cached_ai:
            try:
                aiHtml = open(
                    f"leetcode_cache/ai/{line}.html", "r", encoding="utf-8"
                ).read()
                soup = BeautifulSoup(aiHtml, "html.parser")
                [hr.decompose() for hr in soup.find_all("hr")]
                ai_explanations[idx] = str(soup)
            except FileNotFoundError:
                missing["ai"] += 1
                everythingFound = False
                PrintHelper.print_error("AI Explanation not found.")

        if everythingFound:
            PrintHelper.clear_last_lines(1)

    if missing["q"] == 0 and missing["s"] == 0 and missing["ai"] == 0:
        PrintHelper.print_success("All data found in cache.")
    else:
        PrintHelper.print_warning(
            f"Missing data - Questions: {missing['q']}, Solutions: {missing['s']}, AI Explanations: {missing['ai']}"
        )

    return {
        "table": table,
        "questions": questions,
        "headings": headings,
        "statements": statements,
        "solutions": solutions,
        "ai_explanations": ai_explanations,
    }


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
        PrintHelper.print_info("Processing cached data...")
        data = process_cached_data()
        while True:
            sel = PrintHelper.print_options(
                "Select PDF Type:",
                [
                    "Questions Only",
                    "AI Explanations Only",
                    "Questions + AI Explanations",
                    "==========================================",
                    "Solutions Only",
                    "Questions + Solutions",
                    "Questions + Solutions + AI Explanations",
                    "Back",
                ],
            )
            content = []
            match sel:
                case "Questions Only":
                    content.append("q")
                case "AI Explanations Only":
                    content.append("ai")
                case "Questions + AI Explanations":
                    content.append("q")
                    content.append("ai")
                case "Solutions Only":
                    content.append("s")
                case "Questions + Solutions":
                    content.append("q")
                    content.append("s")
                case "Questions + Solutions + AI Explanations":
                    content.append("q")
                    content.append("s")
                    content.append("ai")
                case "Back":
                    break

            make_pdf(content, data)

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
