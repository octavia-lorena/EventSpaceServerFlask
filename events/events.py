from datetime import date, datetime

from utils import *


# EVENT METHODS

def get_events_by_organizer_id(uid):
    table = get_json_content(events_file_name)
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        if post.get("organizerId") == uid:
            posts.append(post)
    return posts


def get_all_events():
    table = get_json_content(events_file_name)
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        posts.append(post)
    return posts


def existsEvent(id):
    events = get_all_events()
    for event in events:
        if event.get("id") == id:
            return True
    return False


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


@app.post('/event')
def add_event():
    event = request.json
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
    with open(events_file_name, 'w') as f:
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
    with open(events_file_name, 'w') as f:
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
    with open(events_file_name, 'w') as f:
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
    with open(events_file_name, 'w') as f:
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
    with open(events_file_name, 'w') as f:
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
                "status": "Upcoming"
            }
            events[i] = updated_event
            break
    with open(events_file_name, 'w') as f:
        json.dump(events, f)
    return json.dumps(updated_event)


@app.put("/events/past")
def setPastEvents():
    events = get_all_events()
    if len(events) == 0:
        return json.dumps([])
    for i in range(len(events)):
        event = events[i]
        today_date = date.today()
        event_date = datetime.strptime(event.get("date"), '%Y-%m-%d').date()
        print(event_date)
        diff = today_date - event_date
        if int(diff.days) > 0:
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
                "status": "Past"
            }
            events[i] = updated_event
    with open(events_file_name, 'w') as f:
        json.dump(events, f)
    return json.dumps(events)
