import json


def post_as_json(client, url, data):
    return send_as_json(client.post, url, data)


def put_as_json(client, url, data):
    return send_as_json(client.put, url, data)


def send_as_json(method, url, data):
    return method(url, json.dumps(data), "json", HTTP_X_REQUESTED_WITH="XMLHttpRequest")


def get_response_content(response):
    return json.loads(response.content)
