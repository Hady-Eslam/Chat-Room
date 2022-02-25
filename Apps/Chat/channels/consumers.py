from django.http import QueryDict
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from ..models import Members, Messages
from .forms import MessagesForm



class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        self._Member = Members.objects.filter(user=self.scope['user'])\
            .filter(room__code=self.scope['url_route']['kwargs']['room_code'], room__is_deleted=False)\
                .filter(is_deleted=False, is_pending=False).first()
        
        if self._Member is None:
            self.close(403)
            return

        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_groupe_name = 'chat_' + self.room_code

        async_to_sync(self.channel_layer.group_add)(
            self.room_groupe_name,
            self.channel_name
        )

        self.accept()
    

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_groupe_name,
            self.channel_name
        )
    

    def receive_json(self, content, **kwargs):
        _Query = QueryDict('', mutable=True)
        _Query.update({'message': content['message']})
        _Form = MessagesForm(_Query)
        if not _Form.is_valid():
            self.send_json({
                'message': '',
                'errors': _Form.errors.as_json(),
            })
            return 
        
        _Message = Messages(
            user=self._Member.user, room=self._Member.room, message=_Form.cleaned_data['message']
        )
        _Message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_groupe_name,
            {
                'type': 'chat.message',
                'message': {
                    'data': _Message.message,
                    'by': _Message.user.get_short_name(),
                    'created_at': _Message.created_at.isoformat()
                }
            }
        )
    
    def chat_message(self, event):
        self.send_json({
            'message': event['message']
        })
