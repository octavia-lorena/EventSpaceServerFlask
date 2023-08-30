from utils import *


# POST METHODS

def get_posts_by_id(businessId):
    table = get_json_content(posts_file_name)
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        if post.get("businessId") == businessId:
            posts.append(post)
    return posts


def get_post_by_id(id):
    table = get_json_content(posts_file_name)
    if len(table) == 0:
        return []
    posts = []
    for post in table:
        if post.get("id") == id:
            posts.append(post)
    return posts


def get_all_posts_from_json():
    posts = get_json_content(posts_file_name)
    if len(posts) == 0:
        return []
    return posts


def existsPost(postId):
    posts = get_all_posts_from_json()
    for post in posts:
        if post.get("id") == postId:
            return True
    return False


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


@app.post('/post')
def add_post():
    post = request.json
    posts = get_all_posts_from_json()
    if not existsPost(post.get("id")):
        id = generatePostId()
        images = post.get("images").split(';')
        new_post = {"id": id,
                    "businessId": post.get("businessId"),
                    "title": post.get("title"),
                    "description": post.get("description"),
                    "price": post.get("price"),
                    "images": images,
                    "rating": post.get("rating")}
        posts.append(new_post)
    # print(posts.py)
    with open(posts_file_name, 'w') as f:
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
    with open(posts_file_name, 'w') as f:
        json.dump(posts, f)
    return json.dumps(deleted_post)


@app.put('/post/<id>')
def update_post(id):
    posts = get_all_posts_from_json()
    updated_title = request.values.get("title")
    updated_description = request.values.get("description")
    updated_photos = request.values.get("photos")
    print("upd photos: " + updated_photos)
    updated_price = request.values.get("price")
    for i in range(len(posts)):
        if int(posts[i].get("id")) == int(id):
            post = posts[i]
            bid = post.get("businessId")
            photos = updated_photos.split(';')
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
    with open(posts_file_name, 'w') as f:
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
            new_rating["value"] = str(round(
                ((float(new_rating["value"]) * old_count + int(new_value)) / int(new_rating["voterCount"])), 1))
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
    with open(posts_file_name, 'w') as f:
        json.dump(posts, f)
    return json.dumps(post)
