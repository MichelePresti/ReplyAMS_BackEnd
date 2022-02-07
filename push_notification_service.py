import json
import requests
import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.messaging import AndroidNotification, AndroidConfig

serverToken = 'AAAAHeELsu0:APA91bHScmxbmvSuVYswsd5Y2hIUZnwW2yWzVsKILHrRScVvK6vyAjllNcpbWRe3l0aLKZjkK' \
              '-d8c59iJCVZ3ZI67riMYDwxX5K9hJr3xBA_tjlwC23dHH5LdDEsvGQuNw2UrNUDfPTB '

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + serverToken,
}


def init_service(credentialKeyPath):
    cred = credentials.Certificate(credentialKeyPath)
    firebase_admin.initialize_app(cred)


def send_broadcast_notification(topic: str, message: str, priority='high', title='Reply AMS', messageID='NO_ID'):
    """
    tokens = []
    for token in to:
        tokens.append(token)

    config = AndroidConfig(
        priority='high',
        notification=AndroidNotification(priority='max')
        # click_action='FCM_PLUGIN_ACTIVITY',
    )
    message = messaging.Message(
        data={
            'title': title,
            'body': message,
            'type': 'WAKEUP'
        },
        android=config,
        token="fcaDUuoTRDCcCFFsMpAnY6:APA91bHuCXL7xIZ2yioC7EESCTu8B7kQHTVo0236BC_iVdYBwjZJwsLBFa8UcRmfE3b0UN6k9qzl5aEL6a1VL3ZBEy42JigRrN92j0WCr7gJEI4G0x5FEMBGBYiS8jmZomYB8obKGtGR"
    )

    response = messaging.send(message)
    print('{0} messages were sent successfully'.format(response))
    """
    URL = 'https://fcm.googleapis.com/fcm/send'
    data = {
        "to": "/topics/" + topic,
        "data": {
            "message": message,
            "title": title,
            "messageID": messageID
        },
        "priority": priority
    }
    r = requests.post(URL, data=json.dumps(data), headers=headers)
    print(r.content)
