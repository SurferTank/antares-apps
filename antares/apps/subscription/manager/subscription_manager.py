'''
Created on Jul 9, 2016

@author: leobelen
'''
import logging

import js2py

from antares.apps.core.constants import ScriptEngineType
from antares.apps.message.models import Message
from antares.apps.subscription.exceptions.subscription_exception import SubscriptionException
from antares.apps.message.constants import MessageType
from ..constants import EventType
from ..models import SubscriptionEvent

logger = logging.getLogger(__name__)


class SubscriptionManager(object):
    '''
    classdocs
    '''

    @classmethod
    def subscribe_flow_definition(cls, flow_definition):
        SubscriptionEvent.subscribe_flow_definition(flow_definition)

    @classmethod
    def unsubscribe_flow_definition(cls, flow_definition):
        SubscriptionEvent.unsubscribe_flow_definition(flow_definition)

    @classmethod
    def process_document_subscriptions(cls, document):
        from antares.apps.flow.manager import FlowManager
        subs_form_def = Message.find_one_by_form_definition(
            document.get_form_definition())
        if (subs_form_def is None):
            subs_form_def = Message()
            subs_form_def.form_definition = document.get_form_definition()
            subs_form_def.message_type = MessageType.FORM_DEFINITION
            subs_form_def.save()
        subs_event_set = SubscriptionEvent.find_by_source(subs_form_def)

        if (len(subs_event_set) == 0):
            return

        for subs_event in subs_event_set:
            if (subs_event.event_type == EventType.CREATION):
                action_set = subs_event.action_set.select_related().all()
                if (len(action_set) > 0 and
                    ((subs_event.condition_text and SubscriptionManager.
                      _execute_document_subscription_condition(
                          subs_event, document) == True) or
                     not subs_event.condition_text)):
                    for action in action_set:
                        if (action.action_definition.id.lower() ==
                                'create_case' or
                                action.action_definition.lower() ==
                                'createcase'):
                            message = Message.find_or_create_one(
                                document=document)
                            FlowManager.create_case(subs_event, message)

    @classmethod
    def _execute_document_subscription_condition(cls, subs_event, document):
        if subs_event.condition_text is None:
            return True
        condition = subs_event.condition_text
        script_engine = ScriptEngineType.to_enum(subs_event.script_engine)
        if script_engine is None:
            script_engine = ScriptEngineType.JAVASCRIPT
        if script_engine == ScriptEngineType.PYTHON:
            return eval(condition)
        elif script_engine == ScriptEngineType.JAVASCRIPT:
            context = js2py.EvalJs({'document': document})
            return context.eval_js(condition)
        else:
            return False