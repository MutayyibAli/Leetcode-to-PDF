# first line: 37
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
