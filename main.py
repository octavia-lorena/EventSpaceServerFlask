import json
from flask import Flask, request
from datetime import date, datetime
from appointment_request import AppointmentRequest

app = Flask(__name__)

maxPostId = 0
maxRequestId = 0
maxEventId = 0


def get_json_content(file_name):
    with open(file_name, 'r') as f:
        table = json.loads(f.read())
    return table


def get_posts_by_id(businessId):
    table = get_json_content("posts.json")
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        if post.get("businessId") == businessId:
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


def get_max_request_id():
    global maxRequestId
    table = get_json_content("requests.json.json")
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


# POST METHODS

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


@app.put('/post/rate/<id>')
def rate_post(id):
    new_value = request.values.get("ratingValue")
    posts = get_all_posts_from_json()
    for i in range(len(posts)):
        if int(posts[i].get("id")) == int(id):
            post = posts[i]
            new_rating = post.get("rating")
            old_count = int(new_rating["voterCount"])
            new_rating["voterCount"] = str((int(new_rating["voterCount"]) + 1))
            new_rating["value"] = str(
                (float(new_rating["value"]) * old_count + int(new_value)) / int(new_rating["voterCount"]))
            updated_post = {"id": post.get("id"),
                            "businessId": post.get("businessId"),
                            "title": post.get("title"),
                            "description": post.get("description"),
                            "price": post.get("price"),
                            "images": post.get("images"),
                            "rating": new_rating
                            }
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


@app.delete('/request/<id>')
def delete_request(id):
    requests = get_all_requests_from_json()
    for collab_request in requests:
        if int(collab_request.get("id")) == int(id):
            deleted_request = collab_request
            requests.remove(collab_request)
            break
    with open("requests.json", 'w') as f:
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
    with open("requests.json", 'w') as f:
        json.dump(requests, f)
    return json.dumps(deleted_request)


@app.delete('/requests/<eventId>')
def delete_requests_by_event_id(eventId):
    requests = get_all_requests_from_json()
    deleted_request = {}
    for collab_request in requests:
        if int(collab_request.get("eventId")) == int(eventId):
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


# @app.delete('/appointment/<id>')
# def delete_appointment(requestId):
#     requests = get_all_appointments_from_json()
#     for collab_request in requests:
#         if int(collab_request.get("id")) == int(requestId):
#             deleted_request = collab_request
#             requests.remove(collab_request)
#             break
#     with open("appointments.json", 'w') as f:
#         json.dump(requests, f)
#     return json.dumps(deleted_request)


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


@app.get('/business/city/<city>')
def get_businesses_by_city(city):
    businesses = get_all_businesses_from_json()
    b = []
    if len(businesses) == 0:
        return json.dumps([])
    for business in businesses:
        if business.get("city") == str(city):
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


@app.put("/business/<id>")
def update_device_token(id):
    new_token = request.values.get("token")
    businesses = get_all_businesses_from_json()
    for i in range(len(businesses)):
        if businesses[i].get("id") == str(id):
            business = businesses[i]
            updated_business = {
                "id": business.get("id"),
                "businessName": business.get("businessName"),
                "email": business.get("email"),
                "address": business.get("address"),
                "businessType": business.get("businessType"),
                "phoneNumber": business.get("phoneNumber"),
                "lat": business.get("lat"),
                "lng": business.get("lng"),
                "username": business.get("username"),
                "city": business.get("city"),
                "password": business.get("password"),
                "deviceToken": new_token
            }
            businesses[i] = updated_business
            break
    with open("businesses.json", 'w') as f:
        json.dump(businesses, f)
    return json.dumps(business)


# CLIENT METHODS

def get_all_clients_from_json():
    clients = get_json_content("clients.json")
    if len(clients) == 0:
        return []
    return clients


@app.get('/clients')
def get_all_clients():
    clients = get_all_clients_from_json()
    if len(clients) == 0:
        return json.dumps([])
    return json.dumps(clients)


@app.get('/client/<id>')
def get_client_by_id(id):
    clients = get_all_clients_from_json()
    if len(clients) == 0:
        return json.dumps({})
    for business in clients:
        if business.get("id") == id:
            return json.dumps(business)
    return json.dumps({})


def exists_client(id):
    clients = get_appointments_by_client_id()
    for business in clients:
        if business.get("id") == id:
            return True
    return False


@app.post('/client')
def add_client():
    client = request.json
    clients = get_all_clients_from_json()
    if not exists_client(client.get("id")):
        clients.append(client)
    with open("clients.json", 'w') as f:
        json.dump(clients, f)
    return json.dumps(client)


@app.put("/client/<id>")
def update_device_token_client(id):
    new_token = request.values.get("token")
    clients = get_all_clients_from_json()
    for i in range(len(clients)):
        if clients[i].get("id") == str(id):
            client = clients[i]
            updated_client = {
                "id": client.get("id"),
                "firstName": client.get("firstName"),
                "lastName": client.get("lastName"),
                "email": client.get("email"),
                "password": client.get("password"),
                "username": client.get("username"),
                "phoneNumber": client.get("phoneNumber"),
                "deviceToken": new_token
            }
            clients[i] = updated_client
            break
    with open("clients.json", 'w') as f:
        json.dump(clients, f)
    return json.dumps(updated_client)


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


@app.delete('/event/<id>')
def delete_event(id):
    events = get_all_events()
    deleted_event = {}
    for event in events:
        if int(event.get("id")) == int(id):
            today_date = date.today()
            event_date = datetime.strptime(event.get("date"), '%Y-%m-%d').date()
            print(event_date)
            diff = event_date - today_date
            if int(diff.days) > 30:
                deleted_event = event
                events.remove(event)
                break
            else:
                deleted_event = {
                    "id": -1,
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
                break
    with open("events.json", 'w') as f:
        json.dump(events, f)
    return json.dumps(deleted_event)


@app.put('/event/<id>')
def update_event(id):
    events = get_all_events()
    updated_name = request.values.get("name")
    updated_description = request.values.get("description")
    updated_time = request.values.get("time")
    updated_date = request.values.get("date")
    updated_guest_number = request.values.get("guestNumber")
    updated_budget = request.values.get("budget")
    for i in range(len(events)):
        if int(events[i].get("id")) == int(id):
            event = events[i]
            updated_event = {
                "id": id,
                "organizerId": event.get("organizerId"),
                "type": event.get("type"),
                "name": str(updated_name),
                "description": str(updated_description),
                "guestNumber": updated_guest_number,
                "budget": updated_budget,
                "date": str(updated_date),
                "time": str(updated_time),
                "vendors": event.get("vendors"),
                "cost": event.get("cost"),
                "status": event.get("status")}
            events[i] = updated_event
            print(updated_event)
            break
    with open("events.json", 'w') as f:
        json.dump(events, f)
    return json.dumps(event)


@app.put("/event/vendor/<id>")
def set_event_vendor_value(id):
    category = request.values.get("category")
    value = request.values.get("postId")
    events = get_all_events()
    updated_event = {}
    for i in range(len(events)):
        if int(events[i].get("id")) == int(id):
            event = events[i]
            new_vendors = event.get("vendors")
            print(new_vendors)
            for key in new_vendors:
                if str(key) == str(category):
                    new_vendors[key] = int(value)
                    break
            print(new_vendors)
            updated_event = {
                "id": event.get("id"),
                "organizerId": event.get("organizerId"),
                "type": event.get("type"),
                "name": event.get("name"),
                "description": event.get("description"),
                "guestNumber": event.get("guestNumber"),
                "budget": event.get("budget"),
                "date": event.get("date"),
                "time": event.get("time"),
                "vendors": new_vendors,
                "cost": event.get("cost"),
                "status": event.get("status")
            }
            events[i] = updated_event
            break
    with open("events.json", 'w') as f:
        json.dump(events, f)
    return json.dumps(updated_event)


@app.put("/event/cost/<id>")
def set_event_cost(id):
    price = request.values.get("price")
    events = get_all_events()
    updated_event = {}
    for i in range(len(events)):
        if int(events[i].get("id")) == int(id):
            event = events[i]
            new_cost = int(event.get("cost"))
            new_cost += int(price)
            updated_event = {
                "id": event.get("id"),
                "organizerId": event.get("organizerId"),
                "type": event.get("type"),
                "name": event.get("name"),
                "description": event.get("description"),
                "guestNumber": event.get("guestNumber"),
                "budget": event.get("budget"),
                "date": event.get("date"),
                "time": event.get("time"),
                "vendors": event.get("vendors"),
                "cost": new_cost,
                "status": event.get("status")
            }
            events[i] = updated_event
            break
    with open("events.json", 'w') as f:
        json.dump(events, f)
    return json.dumps(updated_event)


@app.put("/event/publish/<id>")
def publish_event(id):
    events = get_all_events()
    updated_event = {}
    for i in range(len(events)):
        if int(events[i].get("id")) == int(id):
            event = events[i]
            updated_event = {
                "id": event.get("id"),
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
                "status": "Pending"
            }
            events[i] = updated_event
            break
    with open("events.json", 'w') as f:
        json.dump(events, f)
    return json.dumps(updated_event)


# REQUESTS METHODS

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
    with open("requests.json", 'w') as f:
        json.dump(requests, f)
    return json.dumps(new_request)


def get_all_requests_from_file():
    with open("requests.json", 'r') as f:
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
    with open("requests.json", 'w') as f:
        json.dump(requests, f)
    return json.dumps(updated_request)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)
