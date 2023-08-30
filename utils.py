import json

from flask import Flask, request

app = Flask(__name__)

maxPostId = 0
maxRequestId = 0
maxEventId = 0
maxClientId = 0
maxBusinessId = 0

# File Names
clients_file_name = "clients/clients.json"
businesses_file_name = "businesses/businesses.json"
events_file_name = "events/events.json"
posts_file_name = "posts/posts.json"
requests_file_name = "appointment_requests/requests.json"
appointments_file_name = "appointments/appointments.json"

# returns the content of a json file
# input: file_name: String, the name of the json file
def get_json_content(file_name):
    with open(file_name, 'r') as f:
        table = json.loads(f.read())
    return table


def get_max_post_id():
    global maxPostId
    table = get_json_content(posts_file_name)
    for post in table:
        currentId = int(post.get("id"))
        if currentId > maxPostId:
            maxPostId = currentId


def get_max_event_id():
    global maxEventId
    table = get_json_content(events_file_name)
    for post in table:
        currentId = int(post.get("id"))
        if currentId > maxEventId:
            maxEventId = currentId


def get_max_request_id():
    global maxRequestId
    table = get_json_content(requests_file_name)
    for post in table:
        currentId = int(post.get("id"))
        if currentId > maxRequestId:
            maxRequestId = currentId


def generatePostId():
    get_max_post_id()
    return maxPostId + 1


def generateEventId():
    get_max_event_id()
    return maxEventId + 1


def generateRequestId():
    get_max_request_id()
    return maxRequestId + 1
