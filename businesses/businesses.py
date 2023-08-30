from utils import *


# BUSINESS OWNER METHODS

def get_businesses_by_id(id):
    tableBusinesses = get_json_content(businesses_file_name)
    if len(tableBusinesses) == 0:
        return []
    businesses = []
    for business in tableBusinesses:
        if business.get("id") == str(id):
            businesses.append(business)
    return businesses


def get_all_businesses_from_json():
    requests = get_json_content(businesses_file_name)
    if len(requests) == 0:
        return []
    return requests


@app.post('/business')
def add_business():
    business = request.json
    businesses = get_all_businesses_from_json()
    new_business = {}
    if not exists_business(business.get("id")):
        new_business = {
            "id": business.get("id"),
            "businessName": business.get("businessName"),
            "email": business.get("email"),
            "address": business.get("address"),
            "businessType": business.get("businessType"),
            "phoneNumber": business.get("phoneNumber"),
            "username": business.get("username"),
            "city": business.get("city"),
            "password": business.get("password"),
            "deviceToken": business.get("deviceToken"),
            "profilePicture": business.get("profilePicture")
        }
        businesses.append(new_business)
    with open(businesses_file_name, 'w') as f:
        json.dump(businesses, f)
    return json.dumps(business)


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


@app.delete('/business/<id>')
def delete_business(id):
    businesses = get_all_businesses_from_json()
    for business in businesses:
        if int(business.get("id")) == int(id):
            deleted_business = business
            businesses.remove(business)
            break
    with open(businesses_file_name, 'w') as f:
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
                "username": business.get("username"),
                "city": business.get("city"),
                "password": business.get("password"),
                "deviceToken": new_token,
                "profilePicture": business.get("profilePicture")
            }
            businesses[i] = updated_business
            break
    with open(businesses_file_name, 'w') as f:
        json.dump(businesses, f)
    return json.dumps(business)
