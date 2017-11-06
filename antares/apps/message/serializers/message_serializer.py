'''
Created on Nov 3, 2017

@author: leobelen
'''
import logging
from rest_framework import serializers
from ..models import Message

logger = logging.getLogger(__name__)

class MessageSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Message
        fields = ('id', 'content')
        read_only_fields = ('creation_date', 'update_date')
