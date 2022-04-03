'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.constants import ScriptEngineType, EnvironmentType, ActionTargetModuleType
from antares.apps.core.models import ActionDefinition
from antares.apps.document.models import FormDefinition
from antares.apps.message.constants import MessageType
from antares.apps.message.models import Message
import logging
import uuid

from django.db import models
from django.utils.translation import gettext as _
from lxml import etree
from lxml import objectify

from ..constants import EventType
from ..exceptions import SubscriptionException
from ..models import SubscriptionAction, SubscriptionActionParameterMap


logger = logging.getLogger(__name__)

NS_MAP = {
    'subs':
    'http://www.surfertank.com/antares/flow/xml/subscriptions',
    'act':
    'http://www.surfertank.com/antares/flow/xml/activityextendedattributes',
    'xpdl':
    'http://www.wfmc.org/2008/XPDL2.1'
}


class SubscriptionEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscriber = models.ForeignKey(
        'message.Message',
        on_delete=models.PROTECT,
        related_name='subscriber_event_set',
        db_column='subscriber',
        blank=True,
        null=True)
    source = models.ForeignKey(
        'message.Message',
        on_delete=models.PROTECT,
        related_name='source_event_set',
        db_column='source',
        blank=True,
        null=True)
    script_engine = models.CharField(max_length=255)
    condition_text = models.CharField(max_length=4000, blank=True, null=True)
    event_type = models.CharField(choices=EventType.choices, max_length=30)
    subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(SubscriptionEvent, self).save(*args, **kwargs)

    @classmethod
    def subscribe_flow_definition(cls, flow_definition):
        subs_node_list = SubscriptionEvent.get_subscription_node(
            flow_definition)
        if (len(subs_node_list) == 0):
            return
        for subs_node in subs_node_list:
            subs_id = subs_node.get('subscriptionId')
            if (subs_id is None):
                raise SubscriptionException(
                    _(__name__ + 'exceptions.missing_subscription_id'))
            subs_event = SubscriptionEvent.find_one_by_subscription_id(subs_id)
            if (subs_event is None):
                SubscriptionEvent._validate_publisher(subs_node)

                subs_event = SubscriptionEvent()
                subs_event.subscription_id = subs_id
                condition = subs_node.find('subs:Condition', namespaces=NS_MAP)
                if (condition is not None and condition.text):
                    subs_event.condition_text = condition.text
                # for now at least.
                subs_event.script_engine = ScriptEngineType.PYTHON
                subs_event.subscriber = Message.find_or_create_one(
                    flow_definition=flow_definition)
                publisher_type_node = MessageType.to_enum(
                    subs_node.find(
                        "subs:Publisher/subs:Type", namespaces=NS_MAP).text)
                if (publisher_type_node == MessageType.FORM_DEFINITION):
                    form_def_node = subs_node.find(
                        'subs:Publisher/subs:Form', namespaces=NS_MAP)
                subs_event.source = Message.find_or_create_one(
                    form_definition=FormDefinition.find_one(
                        form_def_node.text))
                event_type = subs_node.get("eventTrigger")
                if (event_type is not None
                        and EventType.to_enum(event_type) is not None):
                    subs_event.event_type = EventType.to_enum(event_type)
                else:
                    raise SubscriptionException(
                        _(__name__ + 'exceptions.event_trigger_missing'))
                subs_event.save()
                SubscriptionEvent._populate_actions(subs_event, subs_node)

    @classmethod
    def _populate_actions(cls, subs_event, subs_node):
        for action_node in subs_node.iterfind(
                'subs:Actions/subs:Action', namespaces=NS_MAP):
            subs_action_def = SubscriptionAction()
            subs_action_def.event = subs_event
            action_id = action_node.get('id')
            if (action_id and (action_id.lower() == 'createcase'
                               or action_id.lower() == 'create_case')):
                action_def = ActionDefinition.find_one_or_create_by_params(
                    'create_case',
                    environment=EnvironmentType.LOCAL,
                    executable_name='create_case',
                    target_module=ActionTargetModuleType.FLOW)
            subs_action_def.action_definition = action_def
            action_order = subs_node.get('order')
            if (action_order is not None):
                subs_action_def.order_number = int(float(action_order))
            subs_action_def.save()
            SubscriptionEvent._populate_action_parameters(
                subs_action_def, action_node)

    @classmethod
    def _populate_action_parameters(cls, subs_action_def, action_node):
        for parameter_node in action_node.iterfind(
                'subs:Parameters/subs:Parameter', namespaces=NS_MAP):
            param_name = parameter_node.get('id')
            param_content = parameter_node.text
            if (param_content and param_content):
                param_def = SubscriptionActionParameterMap()
                param_def.subscription_action = subs_action_def
                param_def.parameter_name = param_name
                param_def.content_text = param_content
                param_def.save()

    @classmethod
    def get_subscription_node(cls, flow_def):
        """
        Returns the DomList of the subscriptions found for a given flowDef
        """
        xpdl = etree.fromstring(flow_def.flow_package.xpdl)
        for flow_node in xpdl.iterfind(
                'xpdl:WorkflowProcesses/xpdl:WorkflowProcess[@Id="' +
                flow_def.flow_id + '"]',
                namespaces=NS_MAP):
            flow_version = flow_node.find(
                'xpdl:RedefinableHeader/xpdl:Version', namespaces=NS_MAP)
            if (flow_version is not None and flow_version.text
                    and flow_version.text == flow_def.flow_version):
                for subscription_container in flow_node.iterfind(
                        'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                        namespaces=NS_MAP):
                    ea_name = subscription_container.get('Name')
                    if (ea_name is not None
                            and ea_name.lower() == 'subscriptions'):
                        return subscription_container.findall(
                            'subs:Subscriptions/subs:Subscription',
                            namespaces=NS_MAP)
        return []

    @classmethod
    def _validate_publisher(cls, subs_node):
        """
        This method performs two basic controls: that the type corresponds with
         the information provided and that the object exists and can be
         instantiated.
        """
        subs_publisher_type = subs_node.find(
            'subs:Publisher/subs:Type', namespaces=NS_MAP)
        if (subs_publisher_type is None
                or MessageType.to_enum(subs_publisher_type.text) is None):
            raise SubscriptionException(
                _('antares.apps.subscription.service.subscription_event.publisher_is_missing'
                  ))
        if (MessageType.to_enum(
                subs_publisher_type.text) == MessageType.FORM_DEFINITION):
            form_def_node = subs_node.find(
                'subs:Publisher/subs:Form', namespaces=NS_MAP)
            if (form_def_node is not None and form_def_node.text is not None):
                form_def = FormDefinition.find_one(form_def_node.text)
                if (form_def is None):
                    raise SubscriptionException(
                        _(__name__ +
                          'exceptions.form_publisher_wasnt_found {form_def_id}'
                          ).format(form_def_id=form_def_node.text))

        else:
            raise NotImplementedError

    @classmethod
    def unsubscribe_flow_definition(cls, flow_def):
        flow_object = Message.find_one_by_flow_definition(flow_def)
        for event in flow_object.subscriber_event_set.select_related().all():
            for action in event.action_set.select_related().all():
                for action_parameter in action.parameter_set.select_related(
                ).all():
                    action_parameter.delete()
                action.delete()
            event.delete()
        try:
            flow_object.delete()
        except Exception as e:
            pass

    @classmethod
    def find_by_source(cls, source):
        try:
            return SubscriptionEvent.objects.filter(source=source)
        except SubscriptionEvent.DoesNotExist:
            return []

    @classmethod
    def find_by_subscriber(cls, subscriber):
        try:
            return SubscriptionEvent.objects.filter(subscriber=subscriber)
        except SubscriptionEvent.DoesNotExist:
            return []

    @classmethod
    def find_one_by_subscription_id(cls, subscription_id):
        try:
            return SubscriptionEvent.objects.get(
                subscription_id=subscription_id)
        except SubscriptionEvent.DoesNotExist:
            return None

    class Meta:
        app_label = 'subscription'
        db_table = 'subs_event'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
