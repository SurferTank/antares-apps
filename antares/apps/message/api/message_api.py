'''
Created on Nov 3, 2017

@author: leobelen
'''
from rest_framework import generics
from ..serializers import MessageSerializer
from ..models import Message
from rest_framework import permissions
from ..constants import MessageType


class MessageApi(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        """Save the post data when creating a new OptionArbitrageMsg."""
        serializer.save(message_type=MessageType.EXTERNAL_SYSTEM)
