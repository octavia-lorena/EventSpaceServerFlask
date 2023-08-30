from utils import *
from clients.clients import *
from businesses.businesses import *
from events.events import *
from posts.posts import *
from appointment_requests.requests import *
from appointments.appointments import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)
