# test get_slot.py
from datetime import datetime
from utils import get_slot

times = [
    '09:00',
    '09:30',
    '10:00',

    '12:30',
    '13:00',

    '19:00',
    '19:30',
    '20:05'
]

for time in times:
    time = datetime.strptime(time, '%H:%M')
    print(time, get_slot(time))

time = datetime.now()
time = time.strftime('%H:%M')
time = datetime.strptime(time, '%H:%M')
print(time, get_slot(time))