'''
Created on Jul 9, 2016

@author: leobelen
'''
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from antares.apps.core.middleware.request import get_request
from antares.apps.document.models.document_header import DocumentHeader

from ..constants import MessageType


logger = logging.getLogger(__name__)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_definition = models.ForeignKey(
        'flow.FlowDefinition',
        on_delete=models.PROTECT,
        db_column='flow_definition',
        blank=True,
        null=True)
    form_definition = models.ForeignKey(
        'document.FormDefinition',
        on_delete=models.PROTECT,
        db_column='form_definition',
        blank=True,
        null=True)
    flow_case = models.ForeignKey(
        'flow.FlowCase',
        on_delete=models.PROTECT,
        db_column='flow_case',
        blank=True,
        null=True)
    document = models.ForeignKey(
        'document.DocumentHeader',
        on_delete=models.PROTECT,
        db_column='document',
        blank=True,
        null=True)
    client = models.ForeignKey(
        'client.Client',
        on_delete=models.PROTECT,
        db_column='client',
        blank=True,
        null=True)
    concept_type = models.ForeignKey(
        'core.ConceptType',
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    account_type = models.ForeignKey(
        'accounting.AccountType',
        on_delete=models.PROTECT,
        db_column='account_type',
        blank=True,
        null=True)
    period = models.IntegerField(blank=True, null=True)
    message_type = models.CharField(choices=MessageType.choices, max_length=30)
    content = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".creation_name"),
        help_text=_(__name__ + ".creation_name_help"))
    update_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".update_date"),
        help_text=_(__name__ + ".update_date_help"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".author"),
        help_text=_(__name__ + ".author_help"))

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(Message, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @classmethod
    def validate_value(cls, obj):
        obj_type = MessageType.to_enum(obj.type)
        if (obj is None or obj_type is None):
            return False
        if (obj_type == MessageType.CURRENT_ACCOUNT and obj.client is not None
                and obj.concept_type is not None and obj.period is not None
                and obj.account_type is not None):
            return True
        elif (obj_type == MessageType.FORM_DEFINITION
              and obj.form_definition is not None):
            return True
        elif (obj_type == MessageType.FLOW_DEFINITION
              and obj.flow_definition is not None):
            return True
        elif (obj_type == MessageType.FLOW_CASE and obj.form_case is not None):
            return True
        elif (obj_type == MessageType.DOCUMENT and obj.document is not None):
            return True
        else:
            return False

    @classmethod
    def get_value(cls, obj):
        obj_type = MessageType.to_enum(obj.type)
        if (obj is None or obj_type is None):
            return None
        if (obj_type == MessageType.CURRENT_ACCOUNT and obj.client is not None
                and obj.concept_type is not None and obj.period is not None
                and obj.account_type is not None):
            # TODO: we need to figure this out yet.
            pass
        elif (obj_type == MessageType.FORM_DEFINITION
              and obj.form_definition is not None):
            return obj.form_definition
        elif (obj_type == MessageType.FLOW_DEFINITION
              and obj.flow_definition is not None):
            return obj.flow_definition
        elif (obj_type == MessageType.FLOW_CASE and obj.form_case is not None):
            return obj.form_case
        elif (obj_type == MessageType.DOCUMENT and obj.document is not None):
            return obj.document
        else:
            return None

    @classmethod
    def find_or_create_one(cls, **kwargs):
        from antares.apps.document.types import Document
        from antares.apps.flow.models import FlowDefinition
        from antares.apps.document.models import FormDefinition
        flow_definition = kwargs.get('flow_definition')
        if (flow_definition is not None):
            if isinstance(flow_definition, FlowDefinition):
                flow_definition_object = flow_definition
            else:
                raise ValueError
            try:
                subs_object = Message.objects.get(
                    flow_definition=flow_definition_object.id)
                return subs_object
            except Message.DoesNotExist:
                subs_object = Message()
                subs_object.flow_definition = flow_definition_object
                subs_object.message_type = MessageType.FLOW_DEFINITION
                subs_object.save()
                return subs_object

        form_definition = kwargs.get('form_definition')
        if (form_definition is not None):
            if isinstance(form_definition, FormDefinition):
                form_definition_object = form_definition
            else:
                raise ValueError
            try:
                subs_object = Message.objects.get(
                    form_definition=form_definition_object)
                return subs_object
            except Message.DoesNotExist:
                subs_object = Message()
                subs_object.form_definition = form_definition_object
                subs_object.message_type = MessageType.FORM_DEFINITION
                subs_object.save()
                return subs_object

        document = kwargs.get('document')
        if (document is not None):
            if isinstance(document, Document):
                document_object = document.header
            elif isinstance(document, DocumentHeader):
                document_object = document
            else:
                raise ValueError
            try:
                subs_object = Message.objects.get(document=document_object)
                return subs_object
            except Message.DoesNotExist:
                subs_object = Message()
                subs_object.document = document_object
                subs_object.message_type = MessageType.DOCUMENT
                subs_object.save()
                return subs_object
        raise NotImplementedError

    @classmethod
    def find_one_by_flow_definition(cls, flow_def):
        try:
            return Message.objects.get(flow_definition=flow_def)
        except Message.DoesNotExist:
            return None

    @classmethod
    def find_one_by_document(cls, document):
        try:
            return Message.objects.get(document=document)
        except Message.DoesNotExist:
            return None

    @classmethod
    def find_one_by_form_definition(cls, form_def):
        try:
            return Message.objects.get(form_definition=form_def)
        except Message.DoesNotExist:
            return None

    class Meta:
        app_label = 'message'
        db_table = 'msg_message'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
