from channels import Group
from channels.sessions import channel_session
from .models import ChatMessage
from django.contrib.auth.models import User
import json

# Connected to websocket.connect
@channel_session
def ws_connect(message):
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
@channel_session
def ws_message(message):
    tmp = json.loads(message['text'])
    user = User.objects.get(username=tmp['user'])
    ChatMessage.objects.create(
        message=tmp['message'],
        user=user,
        #  timestamp=tmp['timestamp'] # in models it is default=timezone.now
    )
    Group("chat").send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)