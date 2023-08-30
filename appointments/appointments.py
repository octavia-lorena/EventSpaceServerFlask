from utils import *


# APPOINTMENTS METHODS

def get_appointments_by_business_id(uid):
    tablePosts = get_json_content(posts_file_name)
    tableAppointments = get_json_content(appointments_file_name)
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
    tableAppointments = get_json_content(appointments_file_name)
    if len(tableAppointments) == 0:
        return []
    appointments = []
    for appointment in tableAppointments:
        if appointment.get("postId") == uid:
            appointments.append(appointment)
    return appointments


def get_all_appointments_from_json():
    requests = get_json_content(appointments_file_name)
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
    with open(appointments_file_name, 'w') as f:
        json.dump(requests, f)
    return json.dumps(appointment)
