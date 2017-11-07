'''
Created on Nov 3, 2017

@author: leobelen
'''
import logging
from rest_framework import serializers
from ..models import Message
from ..constants import MessageType
logger = logging.getLogger(__name__)


class MessageSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    #id = serializers.UUIDField()
    #flow_definition = serializers.UUIDField()
    #form_definition = serializers.UUIDField()
    #flow_case = serializers.UUIDField()
    #document = serializers.UUIDField()
    #client = serializers.UUIDField()
    #concept_type = serializers.UUIDField()
    #account_type = serializers.UUIDField()
    #period = serializers.IntegerField()
    message_type = serializers.CharField(default=str(MessageType.EXTERNAL_SYSTEM))
    content = serializers.JSONField()

    #creation_date = serializers.DateTimeField()
    #update_date = serializers.DateTimeField()
    #author = serializers.UUIDField()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Message
        fields = ('content', 'message_type')
        read_only_fields = ('creation_date', 'update_date', 'author')
