import urllib.parse


def quote_user_id(user_id: str) -> str:
    return user_id[0] + urllib.parse.quote(user_id[1:].split(":")[0], safe="") + ":" + user_id.split(":")[1]
