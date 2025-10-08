# first line: 58
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
