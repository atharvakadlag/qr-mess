from datetime import datetime
from flask import session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            return f(*args, **kwargs)
        return 'You aint logged in, no page for u!'
    return decorated_function

def get_slot(check_time = None):
    if check_time is None:
        check_time = datetime.now()

    check_time = check_time.strftime('%H:%M')
    check_time = datetime.strptime(check_time, '%H:%M')

    slots = {
        'breakfast': {
            'start': datetime.strptime('7', '%H'),
            'end': datetime.strptime('9', '%H')
        },
        'lunch': {
            'start': datetime.strptime('12', '%H'),
            'end': datetime.strptime('14', '%H')
        },
        'dinner': {
            'start': datetime.strptime('19', '%H'),
            'end': datetime.strptime('21', '%H')
        },
    }

    relaxation = datetime.strptime('15', '%M') # +- 15 minutes

    for slot, times in slots.items():
        if check_time >= times['start'] and check_time <= times['end']:
            return slot

    return None

