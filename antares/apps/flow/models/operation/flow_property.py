import logging
import uuid

from django.db import models
from django.db.transaction import TransactionManagementError
from django.utils.translation import ugettext as _
import js2py

from antares.apps.client.models import Client
from antares.apps.core.constants import FieldDataType
from antares.apps.flow.constants import FlowBasicDataSubtype
from antares.apps.flow.constants import FlowDataType
from antares.apps.flow.models.definition import PropertyDefinition


logger = logging.getLogger(__name__)


class FlowProperty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_definition = models.ForeignKey(
        "PropertyDefinition",
        on_delete=models.PROTECT,
        db_column='property_definition',
        related_name='property_set')
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        db_column='flow_case',
        related_name='property_set')
    clob_value = models.BinaryField(blank=True, null=True)
    data_type = models.CharField(choices=FlowDataType.choices, max_length=30)
    date_value = models.DateTimeField(blank=True, null=True)
    decimal_value = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    integer_value = models.BigIntegerField(blank=True, null=True)
    property_id = models.CharField(max_length=100)
    string_value = models.CharField(max_length=2000, blank=True, null=True)
    sub_data_type = models.CharField(choices=FlowBasicDataSubtype.choices, max_length=30)
    text_value = models.TextField(blank=True, null=True)
    boolean_value = models.NullBooleanField()

    def save(self, *args, **kwargs):
        super(FlowProperty, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def find_one(prop_id):
        try:
            return FlowProperty.objects.get(id=prop_id)
        except FlowProperty.DoesNotExist:
            return None

    @staticmethod
    def find_by_flow_case(flow_case):
        try:
            return FlowProperty.objects.filter(flow_case=flow_case)
        except FlowProperty.DoesNotExist:
            return []

    @staticmethod
    def find_one_by_flow_case_and_property_id(flow_case, property_id):
        try:
            return FlowProperty.objects.get(
                flow_case=flow_case, property_id=property_id)
        except FlowProperty.DoesNotExist:
            return None

    @staticmethod
    def attach_properties_to_case(flow_case):
        for prop_def in PropertyDefinition.find_by_flow_definition(
                flow_case.flow_definition):
            flow_prop = FlowProperty()
            flow_prop.flow_case = flow_case
            flow_prop.property_definition = prop_def
            flow_prop.property_id = prop_def.property_id
            flow_prop.data_type = prop_def.data_type
            if prop_def.data_type == FlowDataType.BASIC:
                flow_prop.sub_data_type = prop_def.sub_data_type
                if prop_def.initial_value is not None:
                    initial_value = FlowProperty._evaluate_initial_value(
                        flow_case, prop_def)
                    if flow_prop.sub_data_type == FlowBasicDataSubtype.STRING:
                        flow_prop.string_value = initial_value
                    elif flow_prop.sub_data_type == FlowBasicDataSubtype.TEXT:
                        flow_prop.text_value = initial_value
                    elif flow_prop.sub_data_type == FlowBasicDataSubtype.INTEGER:
                        if flow_prop.integer_value is not None:
                            flow_prop.integer_value = int(float(initial_value))
                    elif flow_prop.sub_data_type == FlowBasicDataSubtype.FLOAT:
                        if flow_prop.float_value is not None:
                            flow_prop.float_value = float(initial_value)
                    elif flow_prop.sub_data_type == FlowBasicDataSubtype.BOOLEAN:
                        if flow_prop.date_value is not None:
                            flow_prop.date_value = initial_value
                    else:
                        raise NotImplementedError(
                            _(__name__ +
                              ".exceptions.basic_data_type_not_implemented_yet"
                              ))

            else:
                raise NotImplementedError(
                    _(__name__ + ".exceptions.data_type_not_implemented_yet"))
            flow_prop.save()
            flow_case.property_set.add(flow_prop)
        flow_case.save()

    @staticmethod
    def _evaluate_initial_value(flow_case, prop_def):
        # for now, only JS
        if prop_def.initial_value is not None:
            if flow_case.source.document is not None:
                context = js2py.EvalJs({
                    'flow_case': flow_case,
                    'document': flow_case.source.document,
                    'source': flow_case.source,
                    'prop_def': prop_def
                })
            else:
                context = js2py.EvalJs({
                    'flow_case': flow_case,
                    'source': flow_case.source,
                    'prop_def': prop_def
                })
            context.execute('result_value = ' + prop_def.initial_value)
            if hasattr(context, 'result_value'):
                return context.result_value
            else:
                return None
        else:
            return None

    @staticmethod
    def update_property_with_document_and_action(flow_case, document,
                                                 subs_action):
        from antares.apps.document.models.document_header import DocumentHeader
        from antares.apps.document.types.document import Document
        if isinstance(document, DocumentHeader):
            document_object = Document(document_id=document.id)
        else:
            document_object = document
        # TODO: adapt code to work with python too, based on XPDL, for
        # now, only JS will work
        context = js2py.EvalJs({
            'document': document_object,
            'flow_case': flow_case
        })
        for param_def in subs_action.parameter_set.select_related().all():
            if param_def.content_text is not None:
                if (param_def.parameter_name and
                        param_def.parameter_name.lower() == '_flow_client_id'):
                    context.execute('result_value = ' + param_def.content_text)
                    if (hasattr(context, 'result_value')
                            and context.result_value is not None):
                        client = Client.find_one(
                            uuid.UUID(context.result_value))
                        if client is not None:
                            flow_case.client = client
                elif (param_def.parameter_name and
                      param_def.parameter_name.lower() == '_flow_priority'):
                    context.execute('result_value = ' + param_def.content_text)
                    if hasattr(context, 'result_value'):
                        flow_case.priority = context.result_value
                elif (param_def.parameter_name and
                      param_def.parameter_name.lower() == '_flow_case_name'):
                    context.execute('result_value = ' + param_def.content_text)
                    if hasattr(context, 'result_value'):
                        flow_case.case_name = context.result_value
                else:
                    try:
                        prop_def = flow_case.property_set.select_related().get(
                            property_id=param_def.parameter_name)
                    except FlowProperty.DoesNotExist:
                        prop_def = None
                    if prop_def is not None:
                        context.execute('result_value =' +
                                        param_def.content_text)
                        if (hasattr(context, 'result_value')
                                and prop_def.data_type == FlowDataType.BASIC
                                and context.result_value is not None):
                            if (prop_def.sub_data_type ==
                                    FlowBasicDataSubtype.STRING):
                                prop_def.string_value = context.result_value
                            elif (prop_def.sub_data_type ==
                                  FlowBasicDataSubtype.TEXT):
                                prop_def.text_value = context.result_value
                            elif (prop_def.sub_data_type ==
                                  FlowBasicDataSubtype.DATE):
                                prop_def.date_value = context.result_value
                            elif (prop_def.sub_data_type ==
                                  FlowBasicDataSubtype.INTEGER):
                                prop_def.integer_value = int(
                                    float(context.result_value))
                            elif (prop_def.sub_data_type ==
                                  FlowBasicDataSubtype.FLOAT):
                                prop_def.decimal_value = float(
                                    context.result_value)
                            else:
                                raise NotImplementedError(
                                    _(__name__ + ".type_not_implemented_yet"))
                        prop_def.save()

    def update_property_with_value(self, value):
        if self.data_type == FlowDataType.BASIC:
            if self.sub_data_type == FlowBasicDataSubtype.STRING:
                self.string_value = value
            elif self.sub_data_type == FlowBasicDataSubtype.TEXT:
                self.text_value = value
            elif self.sub_data_type == FlowBasicDataSubtype.DATE:
                self.date_value = value
            elif self.sub_data_type == FlowBasicDataSubtype.INTEGER:
                self.integer_value = int(float(value))
            elif self.sub_data_type == FlowBasicDataSubtype.FLOAT:
                self.float_value = float(value)
            elif self.sub_data_type == FlowBasicDataSubtype.BOOLEAN:
                if isinstance(value, bool):
                    self.boolean_value = value
                elif isinstance(value, str):
                    if value.lower() == 'true' or value.lower() == 'yes':
                        self.boolean_value = True
                    elif value.lower() == 'false' or value.lower() == 'no':
                        self.boolean_value = False
            else:
                raise NotImplementedError(
                    _(__name__ + ".type_not_implemented_yet"))
            self.save()

    class Meta:
        db_table = 'flow_property'
        unique_together = (("flow_case", "property_definition"), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
