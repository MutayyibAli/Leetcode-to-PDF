# first line: 22
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
