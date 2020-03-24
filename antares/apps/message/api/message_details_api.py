'''
Created on Nov 3, 2017

@author: leobelen
'''
from rest_framework import generics
from rest_framework import permissions

from ..models import Message
from ..serializers import MessageSerializer


class MessageDetailsApi(generics.RetrieveUpdateDestroyAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
