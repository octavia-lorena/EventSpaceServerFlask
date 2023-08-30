import time
from datetime import date, datetime

from posts.posts import get_posts_by_id
from utils import *
from flask import json
from events.events import get_all_events


# APPOINTMENT REQUESTS METHODS

def get_requests_by_id(uid):
    tablePosts = get_json_content(posts_file_name)
    tableRequests = get_json_content(requests_file_name)
    if len(tableRequests) == 0:
        return []
    requests = []
    postIds = []
    for post in tablePosts:
        if post.get("businessId") == uid:
            postIds.append(post.get("id"))
    for collab_request in tableRequests:
        if collab_request.get("postId") in postIds:
            requests.append(collab_request)
    return requests


def get_all_requests_from_json():
    requests = get_json_content(requests_file_name)
    if len(requests) == 0:
        return []
    return requests


def get_max_request_id():
    global maxRequestId
    table = get_json_content(requests_file_name)
    for collab_request in table:
        currentId = int(collab_request.get("id"))
        if currentId > maxRequestId:
            maxRequestId = currentId


@app.get('/requests/<businessId>')
def get_all_requests(businessId):
    requests = get_requests_by_id(businessId)
    if len(requests) == 0:
        return json.dumps([])
    print(requests)
    return json.dumps(requests)


def exists_request(requestId):
    requests = get_all_requests_from_json()
    for collab_request in requests:
        if collab_request.get("id") == requestId:
            return True
    return False


@app.delete('/request/<id>')
def delete_request(id):
    requests = get_all_requests_from_json()
    for collab_request in requests:
        if int(collab_request.get("id")) == int(id):
            deleted_request = collab_request
            requests.remove(collab_request)
            break
    with open(requests_file_name, 'w') as f:
        json.dump(requests, f)
    return json.dumps(deleted_request)


@app.delete('/appointment/<id>')
def delete_appointment(id):
    requests = get_all_requests_from_json()
    events = get_all_events()
    for collab_request in requests:
        for event in events:
            if int(collab_request.get("id")) == int(id) and int(collab_request.get("eventId")) == int(event.get("id")):
                today_date = date.today()
                event_date = datetime.strptime(event.get("date"), '%Y-%m-%d').date()
                diff = event_date - today_date
                if int(diff.days) > 30:
                    deleted_request = collab_request
                    requests.remove(collab_request)
                    break
    with open(requests_file_name, 'w') as f:
        json.dump(requests, f)
    return json.dumps(deleted_request)


@app.delete('/requests/<eventId>')
def delete_requests_by_event_id(eventId):
    requests = get_all_requests_from_json()
    for collab_request in requests:
        print(collab_request.get("id"))
        if collab_request.get("eventId") == int(eventId):
            print(collab_request.get("id"))
            requests.remove(collab_request)
            time.sleep(5)
    with open(requests_file_name, 'w') as f:
        json.dump(requests, f)
    return json.dumps(requests)


@app.post('/request')
def add_request():
    collab_request = request.json
    requests = get_all_requests_from_json()
    if not exists_request(collab_request.get("id")):
        id = generateRequestId()
        new_request = {
            "id": id,
            "eventId": collab_request.get("eventId"),
            "postId": collab_request.get("postId"),
            "status": collab_request.get("status")

        }
        requests.append(new_request)
    with open(requests_file_name, 'w') as f:
        json.dump(requests, f)
    return json.dumps(new_request)


def get_all_requests_from_file():
    with open(requests_file_name, 'r') as f:
        entities = json.loads(f.read())
    if len(entities) == 0:
        return []
    return entities


@app.get('/requests')
def get_requests():
    requests = get_all_requests_from_file()
    if len(requests) == 0:
        return json.dumps([])
    return json.dumps(requests)


@app.get('/requests/<businessId>')
def get_requests_by_businessId(businessId):
    requests = get_all_requests_from_file()
    posts = get_posts_by_id(businessId)
    if len(requests) == 0:
        return json.dumps([])
    result = []
    for post in posts:
        for request in requests:
            if request.get("postId") == post.get("id"):
                result.append(request)
    return json.dumps(result)


@app.put("/request/<id>")
def update_request_status(id):
    new_status = request.values.get("status")
    requests = get_all_requests_from_json()
    for i in range(len(requests)):
        if int(requests[i].get("id")) == int(id):
            current_request = requests[i]
            updated_request = {
                "id": current_request.get("id"),
                "eventId": current_request.get("eventId"),
                "postId": current_request.get("postId"),
                "status": new_status
            }
            requests[i] = updated_request
            break
    with open(requests_file_name, 'w') as f:
        json.dump(requests, f)
    return json.dumps(updated_request)
