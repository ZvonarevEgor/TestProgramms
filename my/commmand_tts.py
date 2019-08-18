#import vk
import json


data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}
json_string = json.dumps(data)
print(json_string)


session = vk.Session()
api = vk.API(session, v=5.92)


def send_message(user_id, random_id, token, message, attachment):
    api.messages.send(access_token=token, random_id=str(random_id),
                      user_id=str(user_id), message=message,
                      attachment=attachment)


if __name__ == '__main__':
    token = '4445b9e36de798e624a5f47f2c3441c8afb0ef8d9125cefdfce8652b778e2ad4207d9d92900dcb494b1f3'
    user_id = '161801342'
    random_id = '11111111113'
    message = 'Привет'
    data = api.photos.getMessagesUploadServer()
    print(data)
    #attachment = ''
    #send_message(user_id, random_id, token, message, attachment)
