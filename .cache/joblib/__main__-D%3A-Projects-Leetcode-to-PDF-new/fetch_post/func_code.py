# first line: 63
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
