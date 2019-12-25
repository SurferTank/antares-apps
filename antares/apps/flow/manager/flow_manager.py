'''
Created on Jul 11, 2016

@author: leobelen
'''
import logging

from babel.dates import parse_date
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
import js2py

from antares.apps.core.constants import ActionType
from antares.apps.core.constants import SystemModuleType, ScriptEngineType
from antares.apps.core.models import HrnCode
from antares.apps.flow.constants import FlowDataType, FlowBasicDataSubtype
from antares.apps.message.constants import MessageStatusType
from antares.apps.message.constants import MessageType
from antares.apps.message.models.message_status import MessageStatus
from antares.apps.user.models import User

from ..constants import FlowCaseSourceType, FlowCaseStatusType, FlowPriorityType, ActivityType, \
    FlowDocumentRelationshipType, FlowActivityStatusType, ExecutionModeType, TransitionType
from ..exceptions import FlowException
from ..models import ActivityDefinition
from ..models import FlowActionDefinition
from ..models import FlowCase, FlowActivity
from ..models import FlowDefinition
from ..models import FlowDocument, FlowProperty, ActivityLog
from ..models import TransitionDefinition
from .assignment_manager import AssignmentManager


logger = logging.getLogger(__name__)


class FlowManager(object):
    """
    
    """

    def __init__(self, **kwargs):
        pass

    @classmethod
    def create_case(cls, subs_event, message):
        status = MessageStatus.find_or_create_one(
            document=message.document, module=SystemModuleType.FLOW)
        if isinstance(status.status, str):
            message_status = MessageStatusType.to_enum(status.status)
        else:
            message_status = status.status

        if (message_status == MessageStatusType.PENDING):
            if (message.message_type == MessageType.DOCUMENT):
                cls.create_document_based_case(subs_event, message)
            status.status = MessageStatusType.PROCESSED
            status.save()

    @classmethod
    def create_document_based_case(cls, subs_event, message):
        from antares.apps.core.models import HrnCode

        flow_case = FlowCase()
        flow_case.flow_definition = subs_event.subscriber.flow_definition
        flow_case.creation_date = timezone.now()
        flow_case.status = FlowCaseStatusType.CREATED
        flow_case.priority = FlowPriorityType.STANDARD
        flow_case.source = message

        HrnCode.process_flow_case_hrn_script(flow_case)

        flow_case.save()

        FlowDocument.attach_document_to_case(
            flow_case, message.document, FlowDocumentRelationshipType.SOURCE)
        FlowProperty.attach_properties_to_case(flow_case)

        for subs_action in subs_event.action_set.select_related().all():
            FlowProperty.update_property_with_document_and_action(
                flow_case, message.document, subs_action)

        FlowManager._initial_run(flow_case)

        flow_case.save()

    @classmethod
    def _initial_run(cls, flow_case):
        if (flow_case is None
                or flow_case.status != FlowCaseStatusType.CREATED):
            raise FlowException(
                _(__package__ + '.invalid_case_status_for_initial_run'))
        activity_definition_list = ActivityDefinition.find_start_activity_definitions(
            flow_case.flow_definition)
        if (len(activity_definition_list) == 0):
            raise FlowException(
                _(__package__ + '.no_initial_activities_were_found'))
        flow_case.status = FlowCaseStatusType.ACTIVE
        flow_case.status_date = timezone.now()
        activity_list = FlowManager._create_from_activity_definition_list(
            flow_case, activity_definition_list)
        flow_case.save()

        for activity in activity_list:
            FlowManager._execute_activity(activity)

    @classmethod
    def _create_from_activity_definition_list(cls, flow_case,
                                              activity_definition_list):

        activity_list = []
        for activity_def in activity_definition_list:
            activity = FlowActivity()
            activity.activity_definition = activity_def
            activity.flow_case = flow_case
            activity.status = FlowActivityStatusType.CREATED
            # todo: add hrn to this.
            activity.save()
            if (activity_def.activity_type != ActivityType.ROUTE
                    and activity_def.activity_type != ActivityType.SUBFLOW):
                activity.performer = AssignmentManager.get_activity_performer(
                    activity)
            else:
                activity.performer = User.get_system_user()
            HrnCode.process_flow_activity_hrn_script(activity)
            activity.save()
            ActivityLog.register_activity_log(activity)
            activity_list.append(activity)
        return activity_list

    @classmethod
    def _execute_activity(cls, activity):
        if (activity is None
                or (activity.status != FlowActivityStatusType.ACTIVE
                    and activity.status != FlowActivityStatusType.CREATED)):
            raise FlowException(
                _(__package__ + '.invalid_activity_status_for_execution'))
        if activity.activity_definition.start_mode == ExecutionModeType.AUTOMATIC:
            cls.start_activity(activity)
            if activity.activity_definition.finish_mode == ExecutionModeType.AUTOMATIC:
                FlowManager.forward_activity(activity, None, True)

    @classmethod
    def start_activity(cls, activity):
        """
        Starts the activity 
        """
        cls._execute_actions(activity, ActionType.PRE_ACTION)
        activity.status = FlowActivityStatusType.ACTIVE
        activity.status_date = timezone.now()
        activity.start_date = timezone.now()
        if (activity.activity_definition.activity_type != ActivityType.ROUTE
                and activity.activity_definition.activity_type !=
                ActivityType.SUBFLOW):
            AssignmentManager.get_activity_performer(activity)
        activity.save()
        ActivityLog.register_activity_log(activity)

    @classmethod
    def _validate_activity_completion(cls, activity):
        message = ""
        for validation in activity.activity_definition.validation_set.select_related(
        ).all():
            if (validation.validation):
                if (validation.script_type == ScriptEngineType.JAVASCRIPT):
                    properties = activity.flow_case.get_property_dict()
                    properties['activity'] = activity
                    properties['flow_case'] = activity.flow_case
                    properties['logger'] = logger
                    context = js2py.EvalJs(properties)
                    # here we return the values as it is, jst hrn_script and hrn_title
                    context.execute('return_value = ' + validation.validation)
                    if hasattr(context, 'return_value'):
                        if context.return_value == False:
                            if validation.message is not None:
                                message += "<div>{message}</div>".format(
                                    message=validation.message)
                            else:
                                message += "<div>{message}</div>".format(
                                    message=_(
                                        __name__ +
                                        '.validation_exception_found {id}')
                                    .format(id=validation.id))
                else:
                    raise NotImplementedError(
                        _(__name__ + '.language_not_implemented_yet'))
        if message:
            return mark_safe(message)
        else:
            return None

    @classmethod
    def _complete_activity(cls, activity):
        cls._execute_actions(activity, ActionType.POST_ACTION)
        # todo: subscription handling

        activity.status = FlowActivityStatusType.COMPLETED
        activity.status_date = timezone.now()
        activity.completion_date = timezone.now()
        activity.save()
        ActivityLog.register_activity_log(activity)
        return activity

    @classmethod
    def _complete_case(cls, flow_case):
        flow_case.status = FlowCaseStatusType.COMPLETED
        flow_case.status_date = timezone.now()
        flow_case.completion_date = timezone.now()
        flow_case.save()
        return flow_case

    @classmethod
    def _cancel_activity(cls, activity):
        # todo: subscription handling

        activity.status = FlowActivityStatusType.CANCELLED
        activity.status_date = timezone.now()
        activity.cancelation_date = timezone.now()
        activity.save()
        ActivityLog.register_activity_log(activity)
        return activity

    @classmethod
    def _process_transition_condition(cls, flow_case, transition_definition):
        if (transition_definition.condition_text is None):
            return True
        else:
            properties = flow_case.get_property_dict()
            properties['flow_case'] = flow_case
            properties['logger'] = logger
            context = js2py.EvalJs(properties)
            # here we return the values as it is, jst hrn_script and hrn_title
            context.execute('return_value = ' +
                            transition_definition.condition_text)
            if (hasattr(context, 'return_value')):
                return bool(context.return_value)
            else:
                return True

    @classmethod
    def check_activity_definition(cls, activity_definition):
        pass

    @classmethod
    def _get_outbound_transition_list(cls, activity, transition_id):
        outbound_transition_definition_list = []
        transition_definition_list = list(
            TransitionDefinition.find_outgoing_transitions(
                activity.activity_definition))
        if (transition_id):
            for transition_definition in transition_definition_list:
                if (transition_definition.transition_id == transition_id):
                    outbound_transition_definition_list.append(
                        transition_definition)
        else:
            outbound_transition_definition_list = transition_definition_list
        return outbound_transition_definition_list

    @classmethod
    def _get_viable_transition_list(cls, activity, transition_definition_list):
        viable_trans_list = []
        otherwise_trans_list = []
        for transition_definition in transition_definition_list:
            if transition_definition.transition_type == TransitionType.CONDITION:
                if (transition_definition.condition_text
                        and FlowManager._process_transition_condition(
                            activity.flow_case,
                            transition_definition) == True):
                    viable_trans_list.append(transition_definition)
            elif transition_definition.transition_type == TransitionType.NONE:
                viable_trans_list.append(transition_definition)
            elif transition_definition.transition_type == TransitionType.OTHERWISE:
                otherwise_trans_list.append(transition_definition)
        if (len(otherwise_trans_list) > 0):
            return otherwise_trans_list
        elif (len(viable_trans_list) > 0):
            return viable_trans_list
        else:
            return []

    @classmethod
    def forward_activity(cls, activity, transition_id, confirmation):
        return_value = {}
        show_activity_dict = {}
        target_activity_list = []

        message = cls._validate_activity_completion(activity)
        if (message is not None):
            return_value['message'] = message
            return return_value

        transition_definition_list = FlowManager._get_outbound_transition_list(
            activity, transition_id)
        if (len(transition_definition_list) == 0):
            if (transition_id):
                raise FlowException(
                    _(__package__ + '.activity_not_valid_for_forwarding'))
            else:
                FlowManager._complete_activity(activity)
                FlowManager._complete_case(activity.flow_case)

        for transition_definition in transition_definition_list:
            target_activity_list.append(
                transition_definition.to_activity_definition)

        if (confirmation == True):
            target_activity_list = FlowManager._create_from_activity_definition_list(
                activity.flow_case, target_activity_list)
            FlowManager._complete_activity(activity)
            for target_activity in target_activity_list:
                FlowManager._execute_activity(target_activity)
                return

        for target_activity in target_activity_list:
            if (target_activity.display_name):
                show_activity_dict[str(
                    target_activity.id)] = target_activity.display_name
            elif (target_activity.activity_id):
                show_activity_dict[str(
                    target_activity.id)] = target_activity.activity_id
            else:
                show_activity_dict[str(target_activity.id)] = str(
                    target_activity.id)

        return_value['activities'] = show_activity_dict

        return return_value

    @classmethod
    def _execute_actions(cls, activity, action_type):
        """ here we execute the actions 
        """
        for action in FlowActionDefinition.find_by_activity_definition_and_action_type(
                activity.activity_definition, action_type):
            if (action.content is not None
                    and action.script_engine == ScriptEngineType.JAVASCRIPT):
                properties = {}
                properties.update(activity.flow_case.get_property_dict())
                properties['activity'] = activity
                properties['flow_case'] = activity.flow_case
                properties['logger'] = logger
                context = js2py.EvalJs(properties)
                context.execute(action.content)
                for prop in activity.flow_case.property_set.select_related(
                ).all():
                    try:
                        attrib = context.__getattr__(prop.property_id)
                    except js2py.base.PyJsException:
                        attrib = None
                    if attrib is not None:
                        if prop.data_type == FlowDataType.BASIC:
                            if prop.sub_data_type == FlowBasicDataSubtype.STRING:
                                prop.string_value = attrib
                            elif prop.sub_data_type == FlowBasicDataSubtype.TEXT:
                                prop.text_value = attrib
                            elif prop.sub_data_type == FlowBasicDataSubtype.INTEGER:
                                prop.integer_value = int(float(attrib))
                            elif prop.sub_data_type == FlowBasicDataSubtype.FLOAT:
                                prop.float_value = float(attrib)
                            elif prop.sub_data_type == FlowBasicDataSubtype.DATE:
                                prop.text_value = parse_date(attrib)
                            elif prop.sub_data_type == FlowBasicDataSubtype.BOOLEAN:
                                if isinstance(attrib, str):
                                    if attrib.lower() == "true" or attrib.lower(
                                    ) == "yes" or attrib == "1":
                                        prop.boolean_value = True
                                    elif attrib.lower(
                                    ) == "false" or attrib.lower(
                                    ) == "no" or attrib == "0":
                                        prop.boolean_value = False
                                else:
                                    prop.boolean_value = attrib
                            else:
                                raise NotImplementedError(
                                    _(__name__ +
                                      ".exceptions.field_type_not_implemented_executing_actions"
                                      ))

                    prop.save()

            else:
                raise NotImplementedError(
                    _(__name__ + '.language_not_implemented_yet'))
