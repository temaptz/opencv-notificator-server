import requests
import config

def sendPhoto(photo):
   for id in config.TELEGRAM_CHAT_IDS:
      url = 'https://api.telegram.org/bot' + config.TELEGRAM_API_KEY + '/sendPhoto?chat_id=' + id

      requests.post(url, files={
         'photo': ('photo.jpg', photo.tobytes(), 'image/jpeg')
      })
