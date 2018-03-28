from requests import get, post, delete


def _get(url, auth):
    print("get")
    hearders = auth.authed("GET", url)
    return get(url=url, headers=hearders)


def _post(url, auth, data):
    print("post")
    hearders = auth.authed("POST", url, body=data)
    return post(url=url, headers=hearders, data=data)


def _delete(url, auth):
    print("delete")
    hearders = auth.authed("DELETE", url)
    return delete(url=url, headers=hearders)