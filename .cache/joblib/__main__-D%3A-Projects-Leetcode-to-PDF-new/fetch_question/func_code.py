# first line: 31
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
