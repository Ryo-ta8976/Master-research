import requests
from datetime import datetime
from pytz import timezone
import time
import schedule
import subprocess
import os
import log


def job():
    date = datetime.now(timezone('Asia/Tokyo')).strftime('%Y/%m/%d %H:00')
    response = requests.post('http://133.19.62.9:50080/Is_it_snowing', json={'date': date})
    log.log(response.status_code)
    if response.status_code == 200:
        log.log(response.text)
        data = response.text
        if data == 'snowing':
            print(data + ' (;;) ')
            log.log('get snowing')
            call_shell()
        # elif data == 'not snowing':
        else:
            print(data + ' (;;) ')
            log.log('get not snowing')
            call_shell()


def call_shell():
    path = os.path.dirname(os.path.abspath(__file__))
    cmd = '{}/shellscript/manage.sh {}'.format(path, 1)
    subprocess.call(cmd, shell=True)


def main():
    # schedule.every().hour.at(':00').do(job)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    log.log('\nstart job')
    job()
    log.log('end job')


if __name__ == '__main__':
    main()