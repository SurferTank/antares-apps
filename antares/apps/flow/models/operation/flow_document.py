from antares.apps.flow.constants import FlowDocumentRelationshipType
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class FlowDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        db_column='flow_case',
        related_name='document_set')
    document = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='document',
        related_name='flow_document_set')
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()
    relationship = models.CharField(
        choices=FlowDocumentRelationshipType.choices, max_length=30)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        super(FlowDocument, self).save(*args, **kwargs)

    @staticmethod
    def attach_document_to_case(flow_case, document, relationship):
        """
        Attaches a document to the flow Case
        """
        flow_doc = FlowDocument()
        flow_doc.document = document
        flow_doc.flow_case = flow_case
        flow_doc.relationship = relationship
        flow_doc.save()

    @staticmethod
    def find_one(doc_id):
        try:
            return FlowDocument.objects.get(id=doc_id)
        except FlowDocument.DoesNotExist:
            return None

    @staticmethod
    def find_by_flow_case(flow_case):
        try:
            return FlowDocument.objects.filter(flow_case=flow_case)
        except FlowDocument.DoesNotExist:
            return []

    @staticmethod
    def find_one_by_flow_case_and_document(flow_case, document):
        try:
            return FlowDocument.objects.get(
                flow_case=flow_case, document=document.header)
        except FlowDocument.DoesNotExist:
            return None

    class Meta:
        app_label = 'flow'
        db_table = 'flow_document'
        unique_together = (("flow_case", "document"),)
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
