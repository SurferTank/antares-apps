import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from enumfields import EnumField

from antares.apps.core.constants import FieldDataType
from antares.apps.document.constants import DocumentStatusType
from antares.apps.flow.constants import FlowCaseStatusType, FlowDataType, \
    FlowBasicDataSubtype


logger = logging.getLogger(__name__)


class FlowCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(
        "message.Message",
        on_delete=models.PROTECT,
        db_column='source',
        blank=True,
        null=True)
    flow_definition = models.ForeignKey(
        "FlowDefinition",
        on_delete=models.PROTECT,
        db_column='flow_definition',
        related_name='flow_case_set',
        blank=True,
        null=True)
    client = models.ForeignKey(
        "client.Client",
        on_delete=models.PROTECT,
        db_column='client',
        blank=True,
        null=True)
    case_name = models.CharField(max_length=255, blank=True, null=True)
    case_number = models.CharField(max_length=255, blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField()
    priority = models.CharField(max_length=30)
    start_date = models.DateTimeField(blank=True, null=True)
    status = EnumField(FlowCaseStatusType, max_length=30)
    hrn_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_(__name__ + ".hrn_code"),
        help_text=_(__name__ + ".hrn_code_help"))

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        super(FlowCase, self).save(*args, **kwargs)

    @classmethod
    def find_one(cls, flow_case_id):
        try:
            return FlowCase.objects.get(id=flow_case_id)
        except FlowCase.DoesNotExist:
            return None

    @classmethod
    def find_one_by_hrn_code(cls, hrn_code):
        try:
            return FlowCase.objects.get(hrn_code=hrn_code)
        except FlowCase.DoesNotExist:
            return None

    def count_documents_by_form_id(self, form_def_id):
        from antares.apps.document.models import FormDefinition
        form_def = FormDefinition.find_one(form_def_id)
        if (form_def is None):
            logger.info(_(__name__ + '.no_form_found_by_that_id'))
            return 0
        doc_count = self.document_set.select_related().filter(
            document__form_definition=form_def).count()
        return doc_count

    def count_documents_by_form_id_and_status(self, form_def_id, status):
        from antares.apps.document.models import FormDefinition
        if isinstance(status, str):
            status = DocumentStatusType.to_enum(status)
        form_def = FormDefinition.find_one(form_def_id)
        if (form_def is None):
            logger.info(_(__name__ + '.no_form_found_by_that_id'))
            return 0
        doc_count = self.document_set.select_related().filter(
            document__form_definition=form_def).filter(
                document__status=status).count()
        return doc_count

    def get_property_dict(self):
        properties = {}
        for prop in self.property_set.select_related():
            if prop.data_type == FlowDataType.BASIC:
                if prop.sub_data_type == FlowBasicDataSubtype.BOOLEAN:
                    properties[prop.property_id] = prop.boolean_value
                elif prop.sub_data_type == FlowBasicDataSubtype.STRING:
                    properties[prop.property_id] = prop.string_value
                elif prop.sub_data_type == FlowBasicDataSubtype.TEXT:
                    properties[prop.property_id] = prop.text_value
                elif prop.sub_data_type == FlowBasicDataSubtype.INTEGER:
                    properties[prop.property_id] = prop.integer_value
                elif prop.sub_data_type == FlowBasicDataSubtype.FLOAT:
                    properties[prop.property_id] = prop.decimal_value
                elif prop.sub_data_type == FlowBasicDataSubtype.DATE:
                    if prop.date_value is not None:
                        properties[prop.property_id] = str(prop.date_value)
                else:
                    raise NotImplementedError(
                        _(__name__ +
                          ".exceptions.field_type_not_implemented {field_sub_data_type}"
                          ).format(field_sub_data_type=prop.sub_data_type))
        return properties

    def delete_flow_case(self):
        for case_property in self.property_set.select_related().all():
            case_property.delete()
        for transaction in self.flow_transition_set.select_related().all():
            transaction.delete()
        for doc in self.document_set.select_related().all():
            doc.delete()
        for note in self.flow_note_set.select_related().all():
            note.delete()

        for activity in self.flow_activity_set.select_related().all():
            for log in activity.activity_log_set.select_related().all():
                log.delete()
            activity.delete()

        for attachment in self.flow_attachment_set.select_related().all():
            attachment.delete()

        self.delete()

    class Meta:
        app_label = 'flow'
        db_table = 'flow_case'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
