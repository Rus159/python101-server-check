import requests
from time import sleep
import sms
from requests.exceptions import HTTPError


def server_check(prev_status, current_status):
    prev_status = current_status
    try:
        response = requests.get('https://python101.online')
        response.raise_for_status()
    except HTTPError:
        current_status = True
        http_error = True
    except Exception:
        current_status = False
    else:
        current_status = True

    if prev_status and not current_status:
        message = 'python101 оффлайн'
        sms.send_sms(message)
    if not prev_status and current_status:
        if http_error:
            message = 'python101 онлайн, но выдает ошибку ' + str(response.status_code)
        else:
            message = 'python101 онлайн'
        sms.send_sms(message)
    http_error = False
    return [prev_status, current_status]


if __name__ == "__main__":
    prev_status = False
    current_status = False
    while True:
        prev_status, current_status = map(bool, server_check(prev_status, current_status))
        sleep(60)
