import requests
import config
import time


def get_bot_url() -> str:
    return 'https://api.telegram.org/bot' + config.TELEGRAM_API_KEY


def send_photo(photo):
    for chat_id in config.TELEGRAM_CHAT_IDS:
        requests.post(
           get_bot_url() + '/sendPhoto?chat_id=' + str(chat_id),
           files={'photo': ('photo.jpg', photo.tobytes(), 'image/jpeg')}
        )


def get_updates(offset_update_id: int):
    print(get_bot_url()
          + '/getUpdates'
          + (('?offset=' + str(offset_update_id)) if offset_update_id else ''))

    res = requests.get(
        get_bot_url()
        + '/getUpdates'
        + (('?offset=' + str(offset_update_id)) if offset_update_id else '')
    )

    if res:
        json = res.json()

        if json and json['result'] and len(json['result']):
            return json['result']

    return []
