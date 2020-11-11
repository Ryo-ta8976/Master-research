from datetime import datetime
from pytz import timezone

def log(sentence):
    with open('log.txt', 'a') as f:
        date = datetime.now(timezone('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')
        print(f'{sentence} at {date}', file=f)