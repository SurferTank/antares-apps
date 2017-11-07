'''
Created on Nov 3, 2017

@author: leobelen
'''
from rest_framework import mixins
from rest_framework import generics
from ..serializers import MessageSerializer
from ..models import Message
from rest_framework import permissions
from ..constants import MessageType
from ..service import MessageManager


class MessageApi(mixins.ListModelMixin, mixins.CreateModelMixin,
                 generics.GenericAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request.data['message_type'] = str(MessageType.EXTERNAL_SYSTEM)
        MessageManager.process_message(self.request.data['content'])
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    #def perform_create(self, serializer):
    #    """Save the post data when creating a new OptionArbitrageMsg."""
    #    serializer.save(message_type=MessageType.EXTERNAL_SYSTEM)
