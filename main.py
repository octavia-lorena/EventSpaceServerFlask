import json
from flask import Flask, request

app = Flask(__name__)

# POST METHODS

maxPostId = 0
maxRequestId = 0
maxEventId = 0


def get_json_content(file_name):
    with open(file_name, 'r') as f:
        table = json.loads(f.read())
    return table


def get_posts_by_id(uid):
    table = get_json_content("posts.json")
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        if post.get("businessId") == uid:
            posts.append(post)
    return posts


def get_events_by_organizer_id(uid):
    table = get_json_content("events.json")
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        if post.get("organizerId") == uid:
            posts.append(post)
    return posts


def get_all_events():
    table = get_json_content("events.json")
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        posts.append(post)
    return posts


def get_post_by_id(id):
    table = get_json_content("posts.json")
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        if post.get("id") == id:
            posts.append(post)
    return posts


def get_all_posts_from_json():
    posts = get_json_content("posts.json")
    if len(posts) == 0:
        return []
    return posts


def get_max_post_id():
    global maxPostId
    table = get_json_content("posts.json")
    for post in table:
        currentId = int(post.get("id"))
        if currentId > maxPostId:
            maxPostId = currentId


def get_max_event_id():
    global maxEventId
    table = get_json_content("events.json")
    for post in table:
        currentId = int(post.get("id"))
        if currentId > maxEventId:
            maxEventId = currentId


def generatePostId():
    get_max_post_id()
    return maxPostId + 1


def generateEventId():
    get_max_event_id()
    return maxEventId + 1


@app.get('/posts')
def get_all_posts_all():
    posts = get_all_posts_from_json()
    if len(posts) == 0:
        return json.dumps([])
    return json.dumps(posts)


@app.get('/posts/<businessId>')
def get_all_posts(businessId):
    posts = get_posts_by_id(businessId)
    if len(posts) == 0:
        return json.dumps([])
    return json.dumps(posts)


@app.get('/post/<id>')
def get_post_by_id(id):
    posts = get_posts_by_id(id)
    if len(posts) == 0:
        return json.dumps({})
    return json.dumps(posts[0])


def existsPost(postId):
    posts = get_all_posts_from_json()
    for post in posts:
        if post.get("id") == postId:
            return True
    return False


@app.post('/post')
def add_post():
    post = request.json
    # print(post)
    # print(post.get("description"))
    posts = get_all_posts_from_json()
    if not existsPost(post.get("id")):
        id = generatePostId()
        new_post = {"id": id,
                    "businessId": post.get("businessId"),
                    "title": post.get("title"),
                    "description": post.get("description"),
                    "price": post.get("price"),
                    "images": post.get("images"),
                    "rating": post.get("rating")}
        posts.append(new_post)
    # print(posts)
    with open("posts.json", 'w') as f:
        json.dump(posts, f)
    return json.dumps(new_post)


@app.delete('/post/<id>')
def delete_post(id):
    posts = get_all_posts_from_json()
    for post in posts:
        if int(post.get("id")) == int(id):
            deleted_post = post
            posts.remove(post)
            break
    with open("posts.json", 'w') as f:
        json.dump(posts, f)
    return json.dumps(deleted_post)


@app.put('/post/<id>')
def update_post(id):
    posts = get_all_posts_from_json()
    updated_title = request.values.get("title")
    updated_description = request.values.get("description")
    updated_photos = request.values.get("photos")
    updated_price = request.values.get("price")
    for i in range(len(posts)):
        if int(posts[i].get("id")) == int(id):
            post = posts[i]
            bid = post.get("businessId")
            photos = updated_photos.split(',')
            updated_post = {"id": int(id),
                            "businessId": str(bid),
                            "title": str(updated_title),
                            "description": str(updated_description),
                            "price": int(updated_price),
                            "images": photos,
                            "rating": post.get("rating")}
            posts[i] = updated_post
            print(updated_post)
            break
    with open("posts.json", 'w') as f:
        json.dump(posts, f)
    return json.dumps(post)


# COLLABORATION REQUESTS METHODS

def get_requests_by_id(uid):
    tablePosts = get_json_content("posts.json")
    tableRequests = get_json_content("requests.json")
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
    requests = get_json_content("requests.json")
    if len(requests) == 0:
        return []
    return requests


def get_max_request_id():
    global maxRequestId
    table = get_json_content("requests.json")
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


@app.post('/request')
def add_request():
    collab_request = request.json
    requests = get_all_requests_from_json()
    if not exists_request(collab_request.get("id")):
        requests.append(collab_request)
    with open("requests.json", 'w') as f:
        json.dump(requests, f)
    return json.dumps(collab_request)


@app.delete('/request/<id>')
def delete_request(requestId):
    requests = get_all_requests_from_json()
    for collab_request in requests:
        if int(collab_request.get("id")) == int(requestId):
            deleted_request = collab_request
            requests.remove(collab_request)
            break
    with open("requests.json", 'w') as f:
        json.dump(requests, f)
    return json.dumps(deleted_request)


# APPOINTMENTS METHODS

def get_appointments_by_business_id(uid):
    tablePosts = get_json_content("posts.json")
    tableAppointments = get_json_content("appointments.json")
    if len(tableAppointments) == 0:
        return []
    appointments = []
    postIds = []
    for post in tablePosts:
        if post.get("businessId") == uid:
            postIds.append(post.get("id"))
    for appointment in tableAppointments:
        if appointment.get("postId") in postIds:
            appointments.append(appointment)
    return appointments


def get_appointments_by_client_id(uid):
    tableAppointments = get_json_content("appointments.json")
    if len(tableAppointments) == 0:
        return []
    appointments = []
    for appointment in tableAppointments:
        if appointment.get("postId") == uid:
            appointments.append(appointment)
    return appointments


def get_all_appointments_from_json():
    requests = get_json_content("appointments.json")
    if len(requests) == 0:
        return []
    return requests


@app.get('/appointments/business/<businessId>')
def get_all_business_appointments(businessId):
    requests = get_appointments_by_business_id(businessId)
    if len(requests) == 0:
        return json.dumps([])
    print(requests)
    return json.dumps(requests)


@app.get('/appointments/client/<clientId>')
def get_all_client_appointments(clientId):
    requests = get_appointments_by_client_id(clientId)
    if len(requests) == 0:
        return json.dumps([])
    print(requests)
    return json.dumps(requests)


def exists_appointment(requestId):
    requests = get_all_appointments_from_json()
    for collab_request in requests:
        if collab_request.get("id") == requestId:
            return True
    return False


@app.post('/appointment')
def add_appointment():
    appointment = request.json
    requests = get_all_appointments_from_json()
    if not exists_appointment(appointment.get("id")):
        requests.append(appointment)
    with open("appointments.json", 'w') as f:
        json.dump(requests, f)
    return json.dumps(appointment)


@app.delete('/appointment/<id>')
def delete_appointment(requestId):
    requests = get_all_appointments_from_json()
    for collab_request in requests:
        if int(collab_request.get("id")) == int(requestId):
            deleted_request = collab_request
            requests.remove(collab_request)
            break
    with open("appointments.json", 'w') as f:
        json.dump(requests, f)
    return json.dumps(deleted_request)


# BUSINESS OWNER METHODS

def get_businesses_by_id(id):
    tableBusinesses = get_json_content("businesses.json")
    if len(tableBusinesses) == 0:
        return []
    businesses = []
    for business in tableBusinesses:
        if business.get("id") == str(id):
            businesses.append(business)
    return businesses


def get_all_businesses_from_json():
    requests = get_json_content("businesses.json")
    if len(requests) == 0:
        return []
    return requests


@app.get('/business')
def get_all_businesses():
    businesses = get_all_businesses_from_json()
    if len(businesses) == 0:
        return json.dumps([])
    return json.dumps(businesses)


@app.get('/business/<id>')
def get_business_by_id(id):
    businesses = get_all_businesses_from_json()
    if len(businesses) == 0:
        return json.dumps({})
    for business in businesses:
        if business.get("id") == id:
            return json.dumps(business)
    return json.dumps({})


@app.get('/business/type/<type>')
def get_businesses_by_type(type):
    businesses = get_all_businesses_from_json()
    b = []
    if len(businesses) == 0:
        return json.dumps([])
    for business in businesses:
        if business.get("businessType") == str(type):
            b.append(business)
    return json.dumps(b)


def exists_business(id):
    businesses = get_all_businesses_from_json()
    for business in businesses:
        if business.get("id") == id:
            return True
    return False


@app.post('/business')
def add_business():
    business = request.json
    businesses = get_all_businesses_from_json()
    if not exists_business(business.get("id")):
        businesses.append(business)
    with open("businesses.json", 'w') as f:
        json.dump(businesses, f)
    return json.dumps(business)


@app.delete('/business/<id>')
def delete_business(id):
    businesses = get_all_businesses_from_json()
    for business in businesses:
        if int(business.get("id")) == int(id):
            deleted_business = business
            businesses.remove(business)
            break
    with open("businesses.json", 'w') as f:
        json.dump(businesses, f)
    return json.dumps(deleted_business)


# EVENT METHODS
@app.get('/events/<id>')
def get_events_by_organizer(id):
    events = get_events_by_organizer_id(id)
    if len(events) == 0:
        return json.dumps([])
    return json.dumps(events)


@app.get('/event/<id>')
def get_event_by_id(id):
    events = get_all_events()
    if len(events) == 0:
        return json.dumps({})
    for event in events:
        if event.get("id") == id:
            return json.dumps(event)
    return json.dumps({})


@app.get('/events')
def get_events():
    events = get_all_events()
    if len(events) == 0:
        return json.dumps([])
    return json.dumps(events)


def existsEvent(id):
    events = get_all_events()
    for event in events:
        if event.get("id") == id:
            return True
    return False


@app.post('/event')
def add_event():
    event = request.json
    # print(post)
    # print(post.get("description"))
    events = get_all_events()
    if not existsEvent(event.get("id")):
        id = generateEventId()
        print(event)
        new_event = {
            "id": id,
            "organizerId": event.get("organizerId"),
            "type": event.get("type"),
            "name": event.get("name"),
            "description": event.get("description"),
            "guestNumber": event.get("guestNumber"),
            "budget": event.get("budget"),
            "date": event.get("date"),
            "time": event.get("time"),
            "vendors": event.get("vendors"),
            "cost": event.get("cost"),
            "status": event.get("status")
        }
        events.append(new_event)
    # print(posts)
    with open("events.json", 'w') as f:
        json.dump(events, f)
    return json.dumps(new_event)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)
