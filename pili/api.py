from requests import get, post, delete


def _get(url, auth):
    hearders = auth.authed("GET", url)
    return get(url=url, headers=hearders)


def _post(url, auth, data):
    hearders = auth.authed("POST", url, body=data)
    return post(url=url, headers=hearders, data=data)


def _delete(url, auth):
    hearders = auth.authed("DELETE", url)
    return delete(url=url, headers=hearders)