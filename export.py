# import sys
# import os
# import re
# import argparse
# from joblib import Memory
# import requests
# import json
# from types import SimpleNamespace
# import markdown
# import mdformat
# import weasyprint
# from google import genai

# endpoint = open("assets/endpoint.txt").read().strip()
# questionGQL = open("assets/graphql/question.gql").read()
# solutionGQL = open("assets/graphql/solution.gql").read()
# postGQL = open("assets/graphql/post.gql").read()
# styles = open("assets/styles.css").read()

# # Create necessary directories if they don't exist
# os.makedirs("questions_cache", exist_ok=True)
# os.makedirs(".cache", exist_ok=True)

# # Initialize joblib memory for caching
# memory = Memory(".cache", verbose=0)


def print_summary(questions, cachedQuestions):
    newQuestions = [q for q in questions if q not in cachedQuestions]
    print("--------------------------------")
    print("Questions:")
    print(f"  \033[1;33mTotal:  {len(questions)}\033[0m")
    print(f"  \033[32mCached: {len(cachedQuestions)}\033[0m")
    print(f"  \033[31mNew:    {len(newQuestions)}\033[0m")
    print("--------------------------------")


# @memory.cache
# def fetch_question(slug):
#     base = {
#         "operationName": "questionData",
#         "variables": {"titleSlug": slug},
#         "query": questionGQL,
#     }

#     result = requests.get(endpoint, json=base)
#     return json.loads(
#         result.text, object_hook=lambda d: SimpleNamespace(**d)
#     ).data.question


# @memory.cache
# def fetch_solutions(slug, languageTags):
#     base = {
#         "operationName": "solutions",
#         "variables": {
#             "questionSlug": slug,
#             "skip": 0,
#             "first": 1,
#             "orderBy": "most_votes",
#             "languageTags": languageTags,
#         },
#         "query": solutionGQL,
#     }

#     result = requests.get(endpoint, json=base)

#     return json.loads(
#         result.text, object_hook=lambda d: SimpleNamespace(**d)
#     ).data.questionSolutions.solutions


# @memory.cache
# def fetch_post(postId):
#     base = {
#         "operationName": "getPost",
#         "variables": {"postId": postId},
#         "query": postGQL,
#     }

#     result = requests.get(endpoint, json=base)
#     post = json.loads(result.text, object_hook=lambda d: SimpleNamespace(**d)).data.post
#     post.content = bytes(post.content, "utf-8").decode("unicode_escape")

#     return post


def format_solution(post, slug):
    post = re.sub(
        r"^```(\w+)",
        lambda m: f"```{m.group(1)}\nLanguage: {m.group(1)}",
        post,
        flags=re.MULTILINE,
    )
    post = (
        post.replace("../Figures", f"https://leetcode.com/problems/{slug}/Figures")
        .replace("```", "``` ")
        .replace("[]", "")
    )
    post = mdformat.text(post)
    post = markdown.markdown(
        post,
        extensions=["fenced_code", "codehilite", "tables", "nl2br", "sane_lists"],
    )
    post = re.sub(
        r"<h([1-5])>(.*?)</h\1>",
        lambda m: f"<h{str(int(m.group(1)) + 1)}>{m.group(2)}</h{str(int(m.group(1)) + 1)}>",
        post,
    )
    return post


def get_ai_solution(question, cpp_solution, py_solution):
    prompt = (
        "Do not say 'here is' at the beginning or at the end, only provide the output as markdown.\n"
        + "You are an expert programmer and educator. Given a coding problem and solutions, your task is to provide a clear and concise solution.\n"
        + "Output should be as follows:\n"
        + "Explanation of all the different approaches to solution used in above and give time and space complexity of each approach.\n"
        + "Then provide C++ code for the best solution\n"
        + "Then provide Python code for the best solution\n"
        + "\n\nHTML of problem from Leetcode:\n"
        + question
        + "\n\nC++ Solution:\n"
        + cpp_solution
        + "\n\nPython Solution:\n"
        + py_solution
    )

    # General Text & Multi-modal Tasks: gemini-2.5-flash
    # Coding and Complex Reasoning Tasks: gemini-2.5-pro
    client = genai.Client(api_key="AIzaSyBTFBZ22rrSD5yWBYqkwRmAGyp6aWUr--4")
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt,
    )
    return response.text


def fetch_data(question, use_ai):
    if use_ai:
        solutionsC = fetch_solutions(question.titleSlug, ["cpp"])
        postIdC = solutionsC[0].post.id
        postC = fetch_post(postIdC)

        solutionsPy = fetch_solutions(question.titleSlug, ["python", "python3"])
        postIdPy = solutionsPy[0].post.id
        postPy = fetch_post(postIdPy)

        result = get_ai_solution(question.content, postC.content, postPy.content)

        result = mdformat.text(result)
        result = markdown.markdown(
            result,
            extensions=["fenced_code", "codehilite", "tables", "nl2br", "sane_lists"],
        )
        result = re.sub(
            r"<h([1-5])>(.*?)</h\1>",
            lambda m: f"<h{str(int(m.group(1)) + 1)}>{m.group(2)}</h{str(int(m.group(1)) + 1)}>",
            result,
        )

        solution = "<h2>Solution [AI]</h2>"
        solution += result
    else:
        solutions = fetch_solutions(question.titleSlug, ["cpp"])
        postId = solutions[0].post.id
        post = fetch_post(postId)
        solution = f"<h2>{solutions[0].title}</h2>"
        solution += format_solution(post.content, question.titleSlug)

    return solution


def test_output(s):
    htmlContent = "<!DOCTYPE html><html><style>STYLES</style><body>BODY</body></html>"
    with open("assets/styles.css") as f:
        styles = f.read()
        htmlContent = htmlContent.replace("STYLES", styles)
    htmlContent = htmlContent.replace("BODY", s)
    with open(".temp/test.html", "w", encoding="utf-8") as f:
        f.write(htmlContent)

    weasyprint.HTML(string=htmlContent).write_pdf(".temp/test.pdf")


def cache_question(question, use_ai):
    q = fetch_question(question)

    if q.isPaidOnly:
        return False

    s = fetch_data(q, use_ai)

    # Question HTML
    htmlStr = "<div>"
    htmlStr += f"<h2><a href='https://leetcode.com/problems/{question}'>[{q.questionFrontendId}]</a> {q.title}</h2>"
    if q.topicTags:
        tags = ", ".join([topic.name for topic in q.topicTags])
        htmlStr += f"<strong>{q.difficulty}</strong>   Tags: {tags}"
    htmlStr += q.content
    if q.hints:
        htmlStr += "<h3>Hints</h3>"
        htmlStr += "<ul>"
        for hint in q.hints:
            htmlStr += f"<li>{hint}</li>"
        htmlStr += "</ul>"
    htmlStr += "</div>"
    htmlStr += '<p style="page-break-before: always" ></p>'

    # Solution HTML
    htmlStr += "<div>"
    htmlStr += s
    htmlStr += "</div>"
    htmlStr += '<p style="page-break-before: always" ></p>'

    if use_ai:
        with open(f"questions_cache/{question}~ai.html", "w", encoding="utf-8") as f:
            f.write(htmlStr)
    else:
        with open(f"questions_cache/{question}~sol.html", "w", encoding="utf-8") as f:
            f.write(htmlStr)

    # For debugging: write a test HTML file
    # test_output(htmlStr)

    return True


def main():
    # # Parse command-line arguments
    # parser = argparse.ArgumentParser(description="LeetCode to PDF Exporter")
    # parser.add_argument(
    #     "--clear",
    #     action="store_true",
    #     help="Clear the cached questions before running",
    # )
    # parser.add_argument(
    #     "--pdf",
    #     action="store_true",
    #     help="Only create PDF from cached questions",
    # )
    # parser.add_argument(
    #     "--ai",
    #     action="store_true",
    #     help="Use AI to enhance the explanations in the questions",
    # )
    # args = parser.parse_args()

    # Clear cache if --clear flag is set
    # if args.clear:
    #     for file in os.listdir("questions_cache"):
    #         os.remove(os.path.join("questions_cache", file))

    # List all question files in the questions_lists directory
    # files = [f for f in os.listdir("questions_lists") if f.endswith(".txt")]
    # print(f"Found {len(files)} question files.")
    # for idx, filename in enumerate(files, start=1):
    #     print(f"{idx}. {filename}")

    # # Ask user to select a file by serial number
    # while True:
    #     try:
    #         choice = int(
    #             input("Enter the serial number of the file you want to select: ")
    #         )
    #         if 1 <= choice <= len(files):
    #             file = files[choice - 1]
    #             print(f"Selected file: {file}")
    #             break
    #         else:
    #             print(f"Please enter a number between 1 and {len(files)}")
    #     except ValueError:
    #         print("Please enter a valid number.")

    # # Read the selected file
    # try:
    #     file_path = os.path.join("questions_lists", file)
    #     with open(file_path) as f:
    #         lines = f.read().strip().split("\n")
    # except FileNotFoundError:
    #     print(f"Error: {file} not found.")
    #     sys.exit(1)

    questions = [
        line[len("https://leetcode.com/problems/") :].split("/")[0]
        for line in lines
        if line.startswith("https://leetcode.com/problems/")
    ]

    if args.ai:
        cachedQuestions = [
            f[:-8] for f in os.listdir("questions_cache") if f.endswith("~ai.html")
        ]
    else:
        cachedQuestions = [
            f[:-9] for f in os.listdir("questions_cache") if f.endswith("~sol.html")
        ]

    print_summary(questions, cachedQuestions)

    # Cache all the new questions if --pdf flag is not set
    if not args.pdf:
        for idx, question in enumerate(questions):
            print(f"Caching {idx + 1}/{len(questions)}: {question}", end="")
            if question in cachedQuestions:
                isCached = True
            else:
                isCached = cache_question(question, args.ai)

            if isCached:
                print(
                    f"\r\033[32mCached {idx + 1}/{len(questions)}: {question} \033[0m"
                )
            else:
                print(
                    f"\r\033[31mFailed {idx + 1}/{len(questions)}: {question} \033[0m"
                )

    # Make the final HTML
    htmlContent = "<!DOCTYPE html><html><style>STYLES</style><body>BODY</body></html>"
    htmlContent = htmlContent.replace("STYLES", styles)

    # Process each line in the file
    for line in lines:
        if line.startswith("* "):
            # This is a section header
            pass
        else:
            # This is a question link
            pass

    # TODO: Read cached content and place the final combined content here
    htmlContent = htmlContent.replace("BODY", "combined_content")


# if __name__ == "__main__":
#     main()
