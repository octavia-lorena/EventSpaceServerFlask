from utils import *


# CLIENT METHODS

def get_all_clients_from_json():
    clients = get_json_content(clients_file_name)
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
    clients = get_all_clients_from_json()
    for business in clients:
        if business.get("id") == id:
            return True
    return False


@app.post('/client')
def add_client():
    client = request.json
    clients = get_all_clients_from_json()
    new_client = {}
    if not exists_client(client.get("id")):
        new_client = {
            "id": client.get("id"),
            "firstName": client.get("firstName"),
            "lastName": client.get("lastName"),
            "email": client.get("email"),
            "password": client.get("password"),
            "username": client.get("username"),
            "phoneNumber": client.get("phoneNumber"),
            "deviceToken": client.get("deviceToken")
        }
        clients.append(new_client)
    with open(clients_file_name, 'w') as f:
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
    with open(clients_file_name, 'w') as f:
        json.dump(clients, f)
    return json.dumps(updated_client)
