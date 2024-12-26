from app import *
from app import app
from route import *


@app.route('/increment_counter', methods=['PUT', 'Post'])
def increment_counter():




    return 'Cette est destiné à icrémenté une ligne  '