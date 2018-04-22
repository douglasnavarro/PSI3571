from datetime import timedelta, datetime
import random

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

d1 = datetime.strptime('2018-01-01T00:00', '%Y-%m-%dT%H:%M')
d2 = datetime.strptime('2018-04-30T23:59', '%Y-%m-%dT%H:%M')

with open('fake_data.txt', 'w') as f:
    for i in range(10):
        date = random_date(d1,d2).isoformat()
        crowd_list = random.sample(range(1,7), 6)
        crowd_str  = " ".join(str(x) for x in crowd_list)
        line = "0," + date + "," + crowd_str + "\n"
        f.write(line)
        print(line)