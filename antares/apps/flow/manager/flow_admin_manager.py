'''
Created on Jul 4, 2016

@author: leobelen
'''
import logging
import os

import dateutil.parser
from django.utils.translation import ugettext as _
from lxml import etree
from lxml import objectify

from antares.apps.core.constants import ScriptEngineType, FieldDataType, \
    ActionType
from antares.apps.core.constants import TimeUnitType
from antares.apps.core.models import SystemParameter
from antares.apps.document.models.form_definition import FormDefinition
from antares.apps.flow.constants import FlowDefinitionStatusType, FlowAccessLevelType, DefinitionSiteType, PropertyType, FlowDataType, ParticipantType, ActivityType, FlowDefinitionAccessLevelType, FlowPriorityType
from antares.apps.flow.exceptions import InvalidXPDLException, InvalidStatusException
from antares.apps.flow.models.definition.flow_action_definition import FlowActionDefinition
from antares.apps.user.models import Role, OrgUnit, User

from ..constants import ExecutionModeType, FlowBasicDataSubtype, AssignmentStrategyType, TransitionType, FormalParameterModeType, ActivityApplicationDefinitionScopeType, \
    FlowActivityInstantiationType, TimeEstimationMethodType
from ..models import ApplicationDefinition, ApplicationParameterDefinition, ParticipantDefinition, ActivityDefinition, ActivityApplicationDefinition
from ..models import FlowActivityExtraTab, FlowActivityExtraTabParameter, FlowActivityForm, FlowActivityValidation, FlowActivityFormParameter
from ..models import FlowPackage, FlowDefinition, FlowActivity
from ..models import TransitionDefinition, PropertyDefinition, ActivityApplicationParameterDefinition


NS_MAP = {
    'subs':
    'http://www.surfertank.com/antares/flow/xml/subscriptions',
    'act':
    'http://www.surfertank.com/antares/flow/xml/activityextendedattributes',
    'xpdl':
    'http://www.wfmc.org/2008/XPDL2.1'
}

logger = logging.getLogger(__name__)


class FlowAdminManager(object):
    """
    Provides services to load an XPDL to the database
    """

    XPDL_SCHEMA_LOCATION = os.path.dirname(
        os.path.realpath(__file__)) + '/../xml/XPDL21.xsd'

    def __init__(self, **kwargs):
        """
        Sets up the class for further use
        """
        xpdl_string = kwargs.get('xpdl_string')
        xpdl_file = kwargs.get('xpdl_file')
        if (xpdl_file is not None):
            with open(xpdl_file, 'r', encoding='utf8') as file:
                xpdl_string = file.read()

        self.verify_xml_against_schema(xpdl_string)
        self.xpdl = etree.fromstring(xpdl_string)

    def load_xpdl(self):
        """
        Loads the xpdl into the system
        """
        self._check_package_header()
        self._check_processes()
        self._check_package_exists_on_db()
        self._hibernate_package()

    def _check_package_header(self):
        """
        Checks basic information regarding the package to be sure that the XPDL version and the general 
        script engine is valid and supported. 
        """
        xpdl_version = self.xpdl.find(
            'xpdl:PackageHeader/xpdl:XPDLVersion', namespaces=NS_MAP)

        if (xpdl_version is not None and xpdl_version.text != "2.1"):
            raise InvalidXPDLException(
                _(__name__ + ".exceptions.invalid_xpdl_version"))

        package_version = self.xpdl.find(
            'xpdl:RedefinableHeader/xpdl:Version', namespaces=NS_MAP)
        if (package_version is not None and package_version.text is None):
            raise InvalidXPDLException(
                _(__name__ + ".exceptions.null_xpdl_package_version"))

        script_type = self.xpdl.find('xpdl:Script', namespaces=NS_MAP)
        if (not (script_type is not None
                 and script_type.get('Type') is not None
                 and ScriptEngineType.to_enum(
                     script_type.get('Type')) is not None)):
            raise InvalidXPDLException(
                _(__name__ + ".exceptions.invalid_script_engine"))

    def _check_processes(self):
        """
        Checks that processes are defined for the package
        """
        processes = self.xpdl.find(
            'xpdl:WorkflowProcesses/xpdl:WorkflowProcess', namespaces=NS_MAP)
        if (processes is None or len(processes) == 0):
            raise InvalidXPDLException(
                _(__name__ + ".exceptions.no_processes_defined"))

    def _check_package_exists_on_db(self):
        """
        Verifies that the package does not exist on the system.
        """
        logger.debug("we are in the _check_package_exists_on_db method")
        package_id = self.xpdl.get('Id')
        package_version = self.xpdl.find(
            'xpdl:RedefinableHeader/xpdl:Version', namespaces=NS_MAP)
        if (not package_id or package_version is None
                or not package_version.text):
            raise InvalidXPDLException(
                _(__name__ + ".exceptions.package_id_information_is_missing"))
        logger.info("package id " + package_id + ' package_version ' +
                    package_version.text)
        package = FlowPackage.find_one_by_package_id_and_package_version(
            package_id, package_version.text)
        if (package is not None):
            logger.info('package exists')
            raise InvalidXPDLException(
                _(__name__ + ".exceptions.package_already_exists"))
        else:
            logger.info('package does not exist')

    def verify_xml_against_schema(self, xpdl_string):
        """
        Verifies that the XPDL conforms to all schemas. 
        """
        path = os.path.isfile(FlowAdminManager.XPDL_SCHEMA_LOCATION)
        if not path:
            raise FileNotFoundError(
                _(__name__ + ".exceptions.schema_not_found"))

        schema_root = etree.parse(FlowAdminManager.XPDL_SCHEMA_LOCATION)
        schema = etree.XMLSchema(schema_root)

        parser = etree.XMLParser(schema=schema)
        #TODO: until libxml2 solves the issue on validating, this will be out.
        #try:
        #    root = etree.fromstring(xpdl_string, parser)
        #except Exception:
        #    raise InvalidXPDLException(
        #        _(__name__ + ".exceptions.xpdl_is_invalid"))

    def _hibernate_package(self):
        """
        Saves the package to the system.
        """
        package = FlowPackage()
        package_id = self.xpdl.get('Id')
        package_version = self.xpdl.find(
            'xpdl:RedefinableHeader/xpdl:Version', namespaces=NS_MAP)
        if (package_id and package_version is not None
                and package_version.text):
            package.package_id = package_id
            package.package_version = package_version.text

        package_name = self.xpdl.get('Name')
        if (package_name):
            package.package_name = package_name

        package.xpdl = etree.tostring(self.xpdl)
        package.save()
        self._hibernate_workflows(package)
        package.save()

    def _hibernate_workflows(self, package):
        """
        Saves the workflow to the system.
        """
        for workflow_node in self.xpdl.iterfind(
                'xpdl:WorkflowProcesses/xpdl:WorkflowProcess',
                namespaces=NS_MAP):
            flow_def = FlowDefinition()
            flow_def.flow_package = package
            flow_def.status = str(FlowDefinitionStatusType.CREATED)

            flow_name = workflow_node.get('Name')
            if (flow_name):
                flow_def.flow_name = flow_name
            flow_id = workflow_node.get('Id')
            if (flow_id):
                flow_def.flow_id = flow_id
            access_level = workflow_node.get('AccessLevel')
            if (access_level
                    and FlowDefinitionAccessLevelType.to_enum(access_level) is
                    not None):
                flow_def.access_level = FlowDefinitionAccessLevelType.to_enum(
                    access_level)
            else:
                flow_def.access_level = FlowDefinitionAccessLevelType.to_enum(
                    SystemParameter.find_one(
                        "FLOW_DEFINITION_DEFAULT_ACCESS_LEVEL",
                        FieldDataType.STRING,
                        FlowDefinitionAccessLevelType.PUBLIC))
            flow_version = workflow_node.find(
                'xpdl:RedefinableHeader/xpdl:Version', namespaces=NS_MAP)
            if (flow_version is not None and flow_version.text):
                flow_def.flow_version = flow_version.text

            access_level = workflow_node.find(
                'xpdl:RedefinableHeader/xpdl:Version', namespaces=NS_MAP)
            if (access_level is not None and access_level.text
                    and FlowAccessLevelType.to_enum(
                        access_level.text) is not None):
                flow_def.access_level = str(
                    FlowAccessLevelType.to_enum(access_level.text))

            description = workflow_node.find(
                'xpdl:Description', namespaces=NS_MAP)
            if (description is not None and description.text):
                flow_def.description = description.text

            process_header_node = workflow_node.find(
                'xpdl:ProcessHeader', namespaces=NS_MAP)
            if process_header_node is not None:
                if process_header_node.get('DurationUnit') is not None:
                    duration = TimeUnitType.to_enum_from_xpdl(
                        process_header_node.get('DurationUnit'))
                    if duration is not None:
                        flow_def.time_unit = duration
                    else:
                        flow_def.time_unit = TimeUnitType.to_enum(
                            SystemParameter.find_one(
                                "FLOW_DEFINITION_DEFAULT_TIME_UNIT_TYPE",
                                FieldDataType.STRING, TimeUnitType.HOUR.value))
            else:
                flow_def.time_unit = TimeUnitType.to_enum(
                    SystemParameter.find_one(
                        "FLOW_DEFINITION_DEFAULT_TIME_UNIT_TYPE",
                        FieldDataType.STRING, TimeUnitType.HOUR.value))

            priority_node = process_header_node.find(
                'xpdl:Priority', namespaces=NS_MAP)
            if (priority_node is not None and priority_node.text):
                priority = FlowPriorityType.to_enum(priority_node.text)
                if priority is None:
                    priority = FlowPriorityType.to_enum(
                        SystemParameter.find_one(
                            "FLOW_DEFINITION_DEFAULT_PRIORITY",
                            FieldDataType.STRING,
                            FlowPriorityType.STANDARD.value))
                flow_def.priority = priority
            else:
                flow_def.priority = FlowPriorityType.to_enum(
                    SystemParameter.find_one(
                        "FLOW_DEFINITION_DEFAULT_PRIORITY",
                        FieldDataType.STRING, FlowPriorityType.STANDARD.value))

            valid_from_node = process_header_node.find(
                'xpdl:ValidFrom', namespaces=NS_MAP)
            if (valid_from_node is not None and valid_from_node.text):
                flow_def.valid_from = dateutil.parser.parse(
                    valid_from_node.text)

            valid_to_node = process_header_node.find(
                'xpdl:ValidTo', namespaces=NS_MAP)
            if (valid_to_node is not None and valid_to_node.text):
                flow_def.valid_to = dateutil.parser.parse(valid_to_node.text)

            time_estimation_node = process_header_node.find(
                'xpdl:TimeEstimation', namespaces=NS_MAP)
            if time_estimation_node is not None:
                waiting_time_node = time_estimation_node.find(
                    'xpdl:WaitingTime', namespaces=NS_MAP)
                if (waiting_time_node is not None
                        and waiting_time_node.text is not None):
                    flow_def.waiting_time = float(waiting_time_node.text)
                else:
                    flow_def.waiting_time = 0

                working_time_node = time_estimation_node.find(
                    'xpdl:WorkingTime', namespaces=NS_MAP)
                if (working_time_node is not None
                        and working_time_node.text is not None):
                    flow_def.working_time = float(working_time_node.text)
                else:
                    flow_def.working_time = 0

                duration_node = time_estimation_node.find(
                    'xpdl:Duration', namespaces=NS_MAP)
                if (duration_node is not None
                        and duration_node.text is not None):
                    flow_def.duration = float(duration_node.text)
                else:
                    flow_def.duration = 0

                if flow_def.duration != (
                        flow_def.waiting_time + flow_def.working_time):
                    flow_def.duration = (
                        flow_def.waiting_time + flow_def.working_time)
            else:
                flow_def.duration = 0
                flow_def.waiting_time = 0
                flow_def.working_time = 0

            flow_def.save()
            self._hibernate_application_records(package, flow_def,
                                                workflow_node)
            self._hibernate_participant_records(package, flow_def,
                                                workflow_node)
            try:
                self._hibernate_activity_records(package, flow_def,
                                                 workflow_node)
            except Exception as e:
                print(e)

            self._hibernate_transition_records(package, flow_def,
                                               workflow_node)
            self._hibernate_property_records(package, flow_def, workflow_node)
            self.update_flow_definition_time_estimation()
            flow_def.save()
            package.flow_definition_set.add(flow_def)
            package.save()

    def _hibernate_application_records(self, package, flow_def, workflow_node):
        """
        Saves the applications to the system.
        """
        self._create_system_apps(package, flow_def, workflow_node)

        for package_app_node in self.xpdl.iterfind(
                'xpdl:Applications/xpdl:Application', namespaces=NS_MAP):
            self._process_application_records(flow_def, package_app_node,
                                              DefinitionSiteType.PACKAGE)
        for flow_app_node in workflow_node.iterfind(
                'xpdl:Applications/xpdl:Application', namespaces=NS_MAP):
            self._process_application_records(flow_def, flow_app_node,
                                              DefinitionSiteType.FLOW)

    def _create_system_apps(self, package, flow_def, workflow_node):
        """
        Creates the system provided application records and serializes them.
        """
        # update property
        app_def = ApplicationDefinition()
        app_def.flow_definition = flow_def
        app_def.definition_site = DefinitionSiteType.SYSTEM
        app_def.application_id = 'updateproperty'
        app_def.application_name = _(__name__ +
                                     ".manager.default_apps.update_property")
        app_def.save()
        flow_def.application_definition_set.add(app_def)

        prop_def = ApplicationParameterDefinition()
        prop_def.application_definition = app_def
        prop_def.definition_site = DefinitionSiteType.SYSTEM.value
        prop_def.property_type = PropertyType.FORMAL_PARAMETER.value
        prop_def.order_number = 0
        prop_def.data_type = FlowDataType.BASIC.value
        prop_def.parameter_id = 'propertyId'
        prop_def.display_name = 'property ID'
        prop_def.sub_data_type = FlowBasicDataSubtype.STRING.value
        prop_def.save()
        app_def.parameter_definition_set.add(prop_def)
        app_def.save()

        # current account:
        app_def = ApplicationDefinition()
        app_def.flow_definition = flow_def
        app_def.definition_site = DefinitionSiteType.SYSTEM
        app_def.application_id = 'currentaccount'
        app_def.application_name = _(__name__ +
                                     ".manager.default_apps.current_account")
        app_def.route = 'surfertank_antares_account_status_by_client'
        app_def.save()
        flow_def.application_definition_set.add(app_def)

        prop_def = ApplicationParameterDefinition()
        prop_def.application_definition = app_def
        prop_def.definition_site = DefinitionSiteType.SYSTEM
        prop_def.property_type = PropertyType.FORMAL_PARAMETER
        prop_def.order_number = 0
        prop_def.data_type = FlowDataType.BASIC
        prop_def.parameter_id = 'clientId'
        prop_def.display_name = 'Client ID'
        prop_def.sub_data_type = FlowBasicDataSubtype.UUID
        prop_def.save()
        app_def.parameter_definition_set.add(prop_def)
        app_def.save()

    # create document
    # TODO: we need to implement it yet

    def _process_application_records(self, flow_def, app_node,
                                     definition_site):
        """
        Processes the application records to save them to the system. 
        """
        app_def = ApplicationDefinition()
        app_def.flow_definition = flow_def
        app_def.definition_site = definition_site
        app_id = app_node.get('Id')
        if (app_id):
            app_def.application_id = app_id

        app_name = app_node.get('Name')
        if (app_name):
            app_def.application_name = app_name

        description_node = app_node.find('xpdl:Description', namespaces=NS_MAP)
        if (description_node is not None and description_node.text):
            app_def.description = description_node.text

        # lets discover the url and/or route of the app.
        for extended_attribute_node in app_node.iterfind(
                'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                namespaces=NS_MAP):
            if (extended_attribute_node is not None
                    and extended_attribute_node.get('Name')
                    and extended_attribute_node.get('Value')):
                if (extended_attribute_node.get('Name') and
                        extended_attribute_node.get('Name').lower() == 'url'):
                    app_def.url = extended_attribute_node.get('Value')
                elif (extended_attribute_node.get('Name') and
                      extended_attribute_node.get('Name').lower() == 'route'):
                    app_def.route = extended_attribute_node.get('Value')

        app_def.save()
        # now lets add parameters
        i = 0
        for formal_parameter_node in app_node.iterfind(
                'xpdl:FormalParameters/xpdl:FormalParameter',
                namespaces=NS_MAP):
            parameter = ApplicationParameterDefinition()
            parameter.application_definition = app_def
            parameter.definition_site = definition_site
            parameter.property_type = PropertyType.FORMAL_PARAMETER
            parameter.order_number = i
            parameter.data_type = FlowDataType.BASIC
            if (formal_parameter_node.get('Id')):
                parameter.parameter_id = formal_parameter_node.get('Id')
            display_name = formal_parameter_node.find(
                'xpdl:Name', namespaces=NS_MAP)
            if (display_name is not None and display_name):
                parameter.display_name = display_name.text

            sub_data_type = app_node.find(
                'xpdl:DataType/xpdl:BasicType', namespaces=NS_MAP)
            if (sub_data_type is not None and sub_data_type.get('Type')
                    and FieldDataType.to_enum(sub_data_type.get('Type'))):
                parameter.sub_data_type = FieldDataType.to_enum(
                    sub_data_type.get('Type'))
            else:
                parameter.sub_data_type = FieldDataType.STRING

            parameter.save()
            app_def.parameter_definition_set.add(parameter, bulk=False)
            i = i + 1

        app_def.save()

        flow_def.application_definition_set.add(app_def, bulk=False)

    def _hibernate_participant_records(self, package, flow_def, workflow_node):
        """
        Saves the participant records to the system.
        """
        for package_participant_node in self.xpdl.iterfind(
                'xpdl:Participants/xpdl:Participant', namespaces=NS_MAP):
            self._process_participant_records(
                flow_def, package_participant_node, DefinitionSiteType.PACKAGE)
        for flow_participant_node in workflow_node.iterfind(
                'xpdl:Participant/xpdl:Participant', namespaces=NS_MAP):
            self._process_participant_records(flow_def, flow_participant_node,
                                              DefinitionSiteType.FLOW)

    def _process_participant_records(self, flow_def, participant_node,
                                     definition_site):
        """
        Processes the application records to be saved to the system. 
        """
        participant_def = ParticipantDefinition()
        participant_def.flow_definition = flow_def
        participant_def.definition_site = definition_site
        participant_id = participant_node.get('Id')
        if (participant_id):
            participant_def.participant_id = participant_id

        participant_name = participant_node.get('Name')
        if (participant_name):
            participant_def.participant_name = participant_name

        participant_type_node = participant_node.find(
            'xpdl:ParticipantType', namespaces=NS_MAP)
        if (participant_type_node is not None
                and participant_type_node.get('Type') and
                ParticipantType.to_enum(participant_type_node.get('Type'))):
            participant_def.participant_type = ParticipantType.to_enum(
                participant_type_node.get('Type'))

        # lets discover location rules for the participant
        for extended_attribute_node in participant_node.iterfind(
                'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                namespaces=NS_MAP):
            if (extended_attribute_node is not None
                    and extended_attribute_node.get('Name')
                    and extended_attribute_node.get('Value')):
                if (extended_attribute_node.get('Name') and
                        extended_attribute_node.get('Name').lower() == 'role'):
                    participant_role = Role.find_one_by_code(
                        extended_attribute_node.get('Value'))
                    if (participant_role is not None):
                        participant_def.role = participant_role
                    else:
                        raise InvalidXPDLException(
                            _(__name__ +
                              '.exceptions.role_was_not_found_on_system %(role_id)s'
                              ) %
                            {'role_id': extended_attribute_node.get('Value')})
                elif (
                        extended_attribute_node.get('Name') and
                    (extended_attribute_node.get('Name').lower() == 'unit' or
                     extended_attribute_node.get('Name').lower() == 'orgunit')
                ):
                    participant_org_unit = OrgUnit.find_one_by_code(
                        extended_attribute_node.get('Value'))
                    if (participant_org_unit is not None):
                        participant_def.org_unit = participant_org_unit
                    else:
                        raise InvalidXPDLException(
                            _(__name__ +
                              '.exceptions.org_unit_was_not_found_on_system  %(org_unit_id)s'
                              ) % {
                                  'org_unit_id':
                                  extended_attribute_node.get('Value')
                              })
                elif (extended_attribute_node.get('Name').lower() == 'user'):
                    participant_user = User.find_one_by_username(
                        extended_attribute_node.get('Value'))
                    if (participant_user is not None):
                        participant_def.user = participant_user
                    else:
                        raise InvalidXPDLException(
                            _(__name__ +
                              '.exceptions.username_was_not_found_on_system  %(username)s'
                              ) %
                            {'username': extended_attribute_node.get('Value')})
        participant_def.save()
        flow_def.participant_definition_set.add(participant_def)

    def _hibernate_activity_records(self, package, flow_def, workflow_node):
        """
        Saves activity records to the system. 
        """
        for activity_node in workflow_node.iterfind(
                'xpdl:Activities/xpdl:Activity', namespaces=NS_MAP):
            activity_def = ActivityDefinition()
            activity_def.flow_definition = flow_def
            implementation_task_node = activity_node.find(
                'xpdl:Implementation/xpdl:Task', namespaces=NS_MAP)
            implementation_not_impl_node = activity_node.find(
                'xpdl:Implementation', namespaces=NS_MAP)
            if (implementation_task_node is not None):
                activity_def.activity_type = ActivityType.TASK
            elif (implementation_not_impl_node is not None):
                activity_def.activity_type = ActivityType.NO_IMPLEMENTATION
            else:
                # for now at least
                activity_def.activity_type = ActivityType.ROUTE
            activity_id = activity_node.get('Id')
            if (activity_id):
                activity_def.activity_id = activity_id

            activity_name = activity_node.get('Name')
            if (activity_name):
                activity_def.display_name = activity_name

            start_mode = activity_node.get('StartMode')
            if (start_mode
                    and ExecutionModeType.to_enum(start_mode) is not None):
                activity_def.start_mode = ExecutionModeType.to_enum(start_mode)

            finish_mode = activity_node.get('FinishMode')
            if (finish_mode
                    and ExecutionModeType.to_enum(finish_mode) is not None):
                activity_def.finish_mode = ExecutionModeType.to_enum(
                    finish_mode)

            description = activity_node.find(
                'xpdl:Description', namespaces=NS_MAP)
            if (description is not None and description.text):
                activity_def.description = description.text

            simulation_node = activity_node.find(
                'xpdl:SimulationInformation', namespaces=NS_MAP)
            if simulation_node is not None:
                if simulation_node.get('Instantiation'):
                    instantiation = FlowActivityInstantiationType.to_enum(
                        simulation_node)
                    if instantiation is not None:
                        activity_def.instantiation = instantiation
                if activity_def.instantiation is None:
                    activity_def.instantiation = FlowActivityInstantiationType.to_enum(
                        SystemParameter.find_one(
                            "FLOW_ACTIVITY_DEFINITION_DEFAULT_INSTANTIATION",
                            FieldDataType.STRING,
                            FlowActivityInstantiationType.MULTIPLE.value))
                cost_node = simulation_node.find(
                    'xpdl:Cost', namespaces=NS_MAP)
                if (cost_node is not None and cost_node.text is not None):
                    activity_def.cost = cost_node.text
                else:
                    activity_def.cost = "0"

                time_estimation_node = simulation_node.find(
                    'xpdl:TimeEstimation', namespaces=NS_MAP)
                if time_estimation_node is not None:
                    waiting_time_node = time_estimation_node.find(
                        'xpdl:WaitingTime', namespaces=NS_MAP)
                    if (waiting_time_node is not None
                            and waiting_time_node.text is not None):
                        activity_def.waiting_time = float(
                            waiting_time_node.text)
                    else:
                        activity_def.waiting_time = 0

                    working_time_node = time_estimation_node.find(
                        'xpdl:WorkingTime', namespaces=NS_MAP)
                    if (working_time_node is not None
                            and working_time_node.text is not None):
                        activity_def.working_time = float(
                            working_time_node.text)
                    else:
                        activity_def.working_time = 0

                    duration_node = time_estimation_node.find(
                        'xpdl:Duration', namespaces=NS_MAP)
                    if (duration_node is not None
                            and duration_node.text is not None):
                        activity_def.duration = float(duration_node.text)
                    else:
                        activity_def.duration = 0

                    if activity_def.duration != (activity_def.waiting_time +
                                                 activity_def.working_time):
                        activity_def.duration = activity_def.waiting_time + activity_def.working_time
            else:
                activity_def.duration = 0
                activity_def.waiting_time = 0
                activity_def.working_time = 0
                activity_def.cost = 0

            for performer in activity_node.iterfind(
                    'xpdl:Performers/xpdl:Performer', namespaces=NS_MAP):
                if (performer.text):
                    for flow_participant in flow_def.participant_definition_set.select_related(
                    ).all():
                        if (performer.text == flow_participant.participant_id):
                            activity_def.participant_definition_set.add(
                                flow_participant)
            activity_def.save()

            # lets do the tooling
            for tool_node in activity_node.iterfind(
                    'xpdl:Implementation/xpdl:Task/xpdl:TaskApplication',
                    namespaces=NS_MAP):
                tool_id = tool_node.get('Id')

                for activity_tool in flow_def.application_definition_set.select_related(
                ).filter(application_id__iexact=tool_id).all():

                    app_flow_def = ActivityApplicationDefinition()
                    app_flow_def.activity_definition = activity_def
                    app_flow_def.application_definition = activity_tool

                    description_node = tool_node.find(
                        'xpdl:Description', namespaces=NS_MAP)
                    if (description_node is not None
                            and description_node.text):
                        app_flow_def.description = description_node.text
                    ea_node = tool_node.find(
                        'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                        namespaces=NS_MAP)
                    if (ea_node is not None):
                        ea_name = ea_node.get('Name')
                        if (ea_name.lower() == 'scope'):
                            ea_value = ActivityApplicationDefinitionScopeType.to_enum(
                                ea_node.get('Value'))
                            if (ea_value is not None):
                                app_flow_def.scope = ea_value
                            else:
                                app_flow_def.scope = ActivityApplicationDefinitionScopeType.BLANK
                    app_flow_def.save()

                    for param_node in tool_node.iterfind(
                            'xpdl:ActualParameters/xpdl:ActualParameter',
                            namespaces=NS_MAP):
                        tool_param_def = ActivityApplicationParameterDefinition(
                        )
                        tool_param_def.activity_application = app_flow_def
                        tool_param_def.content = param_node.text

                        tool_param_def.save()

            for extended_attribute in activity_node.iterfind(
                    'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                    namespaces=NS_MAP):
                ea_name = extended_attribute.get('Name')
                ea_value = extended_attribute.get('Value')
                if (ea_name and ea_value
                        and ea_name.lower() == 'assigmentstrategy' and
                        AssignmentStrategyType.to_enum(ea_value) is not None):
                    activity_def.assignment_strategy = AssignmentStrategyType.to_enum(
                        ea_value)
                elif (ea_name and ea_name.lower() == 'forms'):
                    for form_node in extended_attribute.iterfind(
                            'act:Forms/act:Form', namespaces=NS_MAP):
                        form_id = form_node.get('id')
                        if (form_id):
                            form_def = FormDefinition.find_one(form_id)
                            if (form_def is not None):
                                activity_form = FlowActivityForm()
                                activity_form.activity_definition = activity_def
                                activity_form.form_definition = form_def
                                can_save = form_node.get('canSave')
                                if (can_save
                                        and (can_save.lower() == 'true'
                                             or can_save.lower() == 'yes')):
                                    activity_form.can_save = True
                                else:
                                    activity_form.can_save = False
                                can_create = form_node.get('canCreate')
                                if (can_create
                                        and (can_create.lower() == 'true'
                                             or can_create.lower() == 'yes')):
                                    activity_form.can_create = True
                                else:
                                    activity_form.can_create = False
                                activity_form.save()
                                for params_node in form_node.iterfind(
                                        'act:Parameters/act:Parameter',
                                        namespaces=NS_MAP):
                                    param_id = params_node.get('id')
                                    if (param_id and params_node.text):
                                        param = FlowActivityFormParameter()
                                        param.param_id = param_id
                                        param.form = activity_form
                                        param.value = params_node.text
                                        param.save()
                elif (ea_name and ea_name.lower() == 'validations'):
                    for validation_node in extended_attribute.iterfind(
                            'act:Validations/act:Validation',
                            namespaces=NS_MAP):
                        validation_id = validation_node.get('id')
                        if (validation_node.text and validation_id):
                            validation = FlowActivityValidation()
                            validation.validation_id = validation_id
                            validation.activity_definition = activity_def
                            validation.validation = validation_node.text
                            validation_message = validation_node.get('message')
                            if (validation_message):
                                validation.message = validation_message
                            validation_script_type = ScriptEngineType.to_enum(
                                validation_node.get('scriptType'))
                            if (validation_script_type):
                                validation.script_type = validation_script_type
                            else:
                                validation.script_type = ScriptEngineType.JAVASCRIPT
                            validation.save()

                elif (ea_name and ea_name.lower() == 'extratabs'):
                    for extra_tabs_node in extended_attribute.iterfind(
                            'act:ActivityTabs/act:ActivityTab',
                            namespaces=NS_MAP):
                        extra_tab_id = extra_tabs_node.get('id')
                        extra_tab_url = extra_tabs_node.get('url')
                        extra_tab_route = extra_tabs_node.get('route')
                        extra_tab_name = extra_tabs_node.get('name')
                        if (extra_tab_id
                                and (extra_tab_url or extra_tab_route)):
                            extra_tab = FlowActivityExtraTab()
                            extra_tab.activity_definition = activity_def
                            extra_tab.tab_id = extra_tab_id
                            if (extra_tab_route):
                                extra_tab.route = extra_tab_route
                            if (extra_tab_url):
                                extra_tab.route = extra_tab_url
                            if (extra_tab_name):
                                extra_tab.tab_name = extra_tab_name
                            else:
                                extra_tab.tab_name = extra_tab_id
                            extra_tab.save()

                            for params_node in extra_tabs_node.iterfind(
                                    'act:Parameters/act:Parameter',
                                    namespaces=NS_MAP):
                                param_id = params_node.get('id')
                                if (param_id and params_node.text):
                                    param = FlowActivityExtraTabParameter()
                                    param.param_id = param_id
                                    param.tab = extra_tab
                                    param.value = params_node.text
                                    param.save()
                elif (ea_name and ea_name.lower() == 'actions'):
                    for action_node in extended_attribute.iterfind(
                            'act:Actions/act:Action', namespaces=NS_MAP):
                        if (action_node.get('Type') is not None):
                            action_type = ActionType.to_enum(
                                action_node.get('Type'))
                        if (action_node.get('ScriptEngine') is not None):
                            script_engine = ScriptEngineType.to_enum(
                                action_node.get('ScriptEngine'))
                        if (action_node.get('Id') is not None):
                            action_id = action_node.get('Id')
                        if (action_type and script_engine):
                            if action_node.text:
                                action_def = FlowActionDefinition()
                                action_def.action_type = action_type
                                action_def.activity_definition = activity_def
                                action_def.content = action_node.text
                                action_def.script_engine = script_engine
                                action_def.save()
                            elif (action_id):
                                raise NotImplementedError

            # some sanity checks
            if (not activity_def.assignment_strategy):
                if (activity_def.activity_type == ActivityType.ROUTE):
                    activity_def.assignment_strategy = AssignmentStrategyType.NONE
                elif (activity_def.activity_type == ActivityType.TASK
                      or activity_def.activity_type ==
                      ActivityType.NO_IMPLEMENTATION):
                    activity_def.assignment_strategy = SystemParameter.find_one(
                        'FLOW_DEFAULT_ACTIVITY_ASSIGNMENT_STRATEGY',
                        FieldDataType.STRING, str(
                            AssignmentStrategyType.RANDOM))

            if (activity_def.start_mode is None):
                if (activity_def.activity_type == ActivityType.ROUTE):
                    activity_def.start_mode = AssignmentStrategyType.NONE
                elif (activity_def.activity_type == ExecutionModeType.AUTOMATIC
                      or activity_def.activity_type ==
                      ActivityType.NO_IMPLEMENTATION):
                    activity_def.start_mode = SystemParameter.find_one(
                        'FLOW_DEFAULT_ACTIVITY_DEFAULT_START_EXECUTION_MODE',
                        FieldDataType.STRING, str(ExecutionModeType.MANUAL))
            if (activity_def.finish_mode is None):
                if (activity_def.activity_type == ActivityType.ROUTE):
                    activity_def.finish_mode = AssignmentStrategyType.NONE
                elif (activity_def.activity_type == ExecutionModeType.AUTOMATIC
                      or activity_def.activity_type ==
                      ActivityType.NO_IMPLEMENTATION):
                    activity_def.finish_mode = SystemParameter.find_one(
                        'FLOW_DEFAULT_ACTIVITY_DEFAULT_FINISH_EXECUTION_MODE',
                        FieldDataType.STRING, str(ExecutionModeType.MANUAL))
            activity_def.save()
            flow_def.activity_definition_set.add(activity_def)
            flow_def.save()

    def _hibernate_transition_records(self, package, flow_def, workflow_node):
        """
        Saves the transitions to the system. 
        """
        for transition_node in workflow_node.iterfind(
                'xpdl:Transitions/xpdl:Transition', namespaces=NS_MAP):
            trans_def = TransitionDefinition()
            trans_def.flow_definition = flow_def
            trans_id = transition_node.get('Id')
            if (trans_id):
                trans_def.transition_id = trans_id

            trans_name = transition_node.get('Name')
            if (trans_name):
                trans_def.transition_name = trans_name

            condition_node = transition_node.find(
                'xpdl:Condition', namespaces=NS_MAP)
            if (condition_node is not None):
                if (condition_node.get('Type') and TransitionType.to_enum(
                        condition_node.get('Type')) is not None):
                    trans_def.transition_type = TransitionType.to_enum(
                        condition_node.get('Type'))
                if (condition_node.text):
                    trans_def.condition_text = condition_node.text

            if (transition_node.get('From')):
                from_activity_definition = flow_def.activity_definition_set.select_related(
                ).get(activity_id=transition_node.get('From'))
                if (from_activity_definition):
                    trans_def.from_activity_definition = from_activity_definition
                else:
                    raise InvalidXPDLException(
                        _(__name__ +
                          '.exceptions.from_activity_id_was_not_found %(transaction_id)s %(activity_id)s'
                          ) % {
                              'transaction_id': trans_id,
                              'activity_id': transition_node.get('From')
                          })

            if (transition_node.get('To')):
                to_activity_definition = flow_def.activity_definition_set.select_related(
                ).get(activity_id=transition_node.get('To'))
                if (from_activity_definition):
                    trans_def.to_activity_definition = to_activity_definition
                else:
                    raise InvalidXPDLException(
                        _(__name__ +
                          '.exceptions.to_activity_id_was_not_found %(transaction_id)s %(activity_id)s'
                          ) % {
                              'transaction_id': trans_id,
                              'activity_id': transition_node.get('To')
                          })
            if trans_def.transition_type is None:
                trans_def.transition_type = TransitionType.NONE

            trans_def.save()
            flow_def.transition_definition_set.add(trans_def)
            flow_def.save()

    def _hibernate_property_records(self, package, flow_def, workflow_node):
        """
        Saves the property definition to be used by the flow to the system. 
        
        There are 4 sources of properties, DataField and Property, both from 
        the package and the flow.
        
        """
        for field_node in self.xpdl.iterfind(
                'xpdl:DataFields/xpdl:DataField', namespaces=NS_MAP):
            prop_def = PropertyDefinition()
            prop_def.flow_definition = flow_def
            prop_def.definition_site = DefinitionSiteType.PACKAGE
            prop_def.property_type = PropertyType.DATA_FIELD
            # we only support this for now. We should do it better.
            prop_def.data_type = FlowDataType.BASIC
            prop_id = field_node.get('Id')
            if (prop_id):
                prop_def.property_id = prop_id
            prop_name = field_node.get('Name')
            if (prop_name):
                prop_def.display_name = prop_name

            sub_data_type_node = field_node.find(
                'xpdl:DataType/xpdl:BasicType', namespaces=NS_MAP)
            if (sub_data_type_node is not None
                    and sub_data_type_node.get('Type')
                    and FlowBasicDataSubtype.to_enum(
                        sub_data_type_node.get('Type')) is not None):
                prop_def.sub_data_type = FlowBasicDataSubtype.to_enum(
                    sub_data_type_node.get('Type'))

            initial_value_node = field_node.find(
                'xpdl:InitialValue', namespaces=NS_MAP)
            if (initial_value_node is not None):
                if (initial_value_node.text):
                    prop_def.initial_value = initial_value_node.text
                if (initial_value_node.get('ScriptType')
                        and ScriptEngineType.to_enum(
                            initial_value_node.get('ScriptType')) is not None):
                    prop_def.script_engine = ScriptEngineType.to_enum(
                        initial_value_node.get('ScriptType'))
                else:
                    prop_def.script_engine = SystemParameter.find_one(
                        "FLOW_PROPERTY_DEFAULT_SCRIPT_LANGUAGE",
                        FieldDataType.STRING, ScriptEngineType.JAVASCRIPT)
            length_node = field_node.find('xpdl:Length', namespaces=NS_MAP)
            if (length_node is not None and length_node.text):
                prop_def.length = int(float(length_node.text))

            ea_node = field_node.find(
                'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                namespaces=NS_MAP)
            if (ea_node is not None):
                ea_name = ea_node.get('Name')
                ea_value = ea_node.get('Value')
                if (ea_name and ea_name.lower() == 'catalog'):
                    prop_def.catalog = ea_value

            prop_def.save()

            flow_def.property_definition_set.add(prop_def)
            flow_def.save()

        for field_node in workflow_node.iterfind(
                'xpdl:DataFields/xpdl:DataField', namespaces=NS_MAP):
            prop_def = PropertyDefinition()
            prop_def.flow_definition = flow_def
            prop_def.definition_site = DefinitionSiteType.FLOW
            prop_def.property_type = PropertyType.DATA_FIELD
            # we only support this for now. We should do it better.
            prop_def.data_type = FlowDataType.BASIC
            prop_id = field_node.get('Id')
            if (prop_id):
                prop_def.property_id = prop_id
            prop_name = field_node.get('Name')
            if (prop_name):
                prop_def.display_name = prop_name

            sub_data_type_node = field_node.find(
                'xpdl:DataType/xpdl:BasicType', namespaces=NS_MAP)
            if (sub_data_type_node is not None
                    and sub_data_type_node.get('Type')
                    and FlowBasicDataSubtype.to_enum(
                        sub_data_type_node.get('Type')) is not None):
                prop_def.sub_data_type = FlowBasicDataSubtype.to_enum(
                    sub_data_type_node.get('Type'))

            initial_value_node = field_node.find(
                'xpdl:InitialValue', namespaces=NS_MAP)
            if (initial_value_node is not None):
                if (initial_value_node.text):
                    prop_def.initial_value = initial_value_node.text
                if (initial_value_node.get('ScriptType')
                        and ScriptEngineType.to_enum(
                            initial_value_node.get('ScriptType')) is not None):
                    prop_def.script_engine = ScriptEngineType.to_enum(
                        initial_value_node.get('ScriptType'))
                else:
                    prop_def.script_engine = SystemParameter.find_one(
                        "FLOW_PROPERTY_DEFAULT_SCRIPT_LANGUAGE",
                        FieldDataType.STRING, ScriptEngineType.JAVASCRIPT)

            length_node = field_node.find('xpdl:Length', namespaces=NS_MAP)
            if (length_node is not None and length_node.text):
                prop_def.length = int(float(length_node.text))

            ea_node = field_node.find(
                'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                namespaces=NS_MAP)
            if (ea_node is not None):
                ea_name = ea_node.get('Name')
                ea_value = ea_node.get('Value')
                if (ea_name and ea_name.lower() == 'catalog'):
                    prop_def.catalog = ea_value

            prop_def.save()

            flow_def.property_definition_set.add(prop_def)
            flow_def.save()

        for field_node in self.xpdl.iterfind(
                'xpdl:FormalParameters/xpdl:FormalParameter',
                namespaces=NS_MAP):
            prop_def = PropertyDefinition()
            prop_def.flow_definition = flow_def
            prop_def.definition_site = DefinitionSiteType.PACKAGE
            prop_def.property_type = PropertyType.FORMAL_PARAMETER
            # we only support this for now. We should do it better.
            prop_def.data_type = FlowDataType.BASIC
            prop_id = field_node.get('Id')
            if (prop_id):
                prop_def.property_id = prop_id
            prop_name = field_node.get('Name')
            if (prop_name):
                prop_def.display_name = prop_name

            sub_data_type_node = field_node.find(
                'xpdl:DataType/xpdl:BasicType', namespaces=NS_MAP)
            if (sub_data_type_node is not None
                    and sub_data_type_node.get('Type')
                    and FlowBasicDataSubtype.to_enum(
                        sub_data_type_node.get('Type')) is not None):
                prop_def.sub_data_type = FlowBasicDataSubtype.to_enum(
                    sub_data_type_node.get('Type'))

            initial_value_node = field_node.find(
                'xpdl:InitialValue', namespaces=NS_MAP)
            if (initial_value_node is not None):
                if (initial_value_node.text):
                    prop_def.initial_value = initial_value_node.text
                if (initial_value_node.get('ScriptType')
                        and ScriptEngineType.to_enum(
                            initial_value_node.get('ScriptType')) is not None):
                    prop_def.script_engine = ScriptEngineType.to_enum(
                        initial_value_node.get('ScriptType'))
                else:
                    prop_def.script_engine = SystemParameter.find_one(
                        "FLOW_PROPERTY_DEFAULT_SCRIPT_LANGUAGE",
                        FieldDataType.STRING, ScriptEngineType.JAVASCRIPT)

            length_node = field_node.find('xpdl:Length', namespaces=NS_MAP)
            if (length_node is not None and length_node.text):
                prop_def.length = int(float(length_node.text))

            ea_node = field_node.find(
                'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                namespaces=NS_MAP)
            if (ea_node is not None):
                ea_name = ea_node.get('Name')
                ea_value = ea_node.get('Value')
                if (ea_name and ea_name.lower() == 'catalog'):
                    prop_def.catalog = ea_value

            formal_param_mode = field_node.get('Mode')
            if (formal_param_mode
                    and FormalParameterModeType.to_enum(formal_param_mode) is
                    not None):
                prop_def.mode = FormalParameterModeType.to_enum(
                    formal_param_mode)
            else:
                prop_def.mode = FormalParameterModeType.IN

            prop_def.save()

            flow_def.property_definition_set.add(prop_def)
            flow_def.save()

        for field_node in workflow_node.iterfind(
                'xpdl:FormalParameters/xpdl:FormalParameter',
                namespaces=NS_MAP):
            prop_def = PropertyDefinition()
            prop_def.flow_definition = flow_def
            prop_def.definition_site = DefinitionSiteType.FLOW
            prop_def.property_type = PropertyType.FORMAL_PARAMETER
            # we only support this for now. We should do it better.
            prop_def.data_type = FlowDataType.BASIC
            prop_id = field_node.get('Id')
            if (prop_id):
                prop_def.property_id = prop_id
            prop_name = field_node.get('Name')
            if (prop_name):
                prop_def.display_name = prop_name

            sub_data_type_node = field_node.find(
                'xpdl:DataType/xpdl:BasicType', namespaces=NS_MAP)
            if (sub_data_type_node is not None
                    and sub_data_type_node.get('Type')
                    and FlowBasicDataSubtype.to_enum(
                        sub_data_type_node.get('Type')) is not None):
                prop_def.sub_data_type = FlowBasicDataSubtype.to_enum(
                    sub_data_type_node.get('Type'))

            initial_value_node = field_node.find(
                'xpdl:InitialValue', namespaces=NS_MAP)
            if (initial_value_node is not None):
                if (initial_value_node.text):
                    prop_def.initial_value = initial_value_node.text
                if (initial_value_node.get('ScriptType')
                        and ScriptEngineType.to_enum(
                            initial_value_node.get('ScriptType')) is not None):
                    prop_def.script_engine = ScriptEngineType.to_enum(
                        initial_value_node.get('ScriptType'))
                else:
                    prop_def.script_engine = SystemParameter.find_one(
                        "FLOW_PROPERTY_DEFAULT_SCRIPT_LANGUAGE",
                        FieldDataType.STRING, ScriptEngineType.JAVASCRIPT)

            length_node = field_node.find('xpdl:Length', namespaces=NS_MAP)
            if (length_node is not None and length_node.text):
                prop_def.length = int(float(length_node.text))

            formal_param_mode = field_node.get('Mode')
            if (formal_param_mode
                    and FormalParameterModeType.to_enum(formal_param_mode) is
                    not None):
                prop_def.mode = FormalParameterModeType.to_enum(
                    formal_param_mode)
            else:
                prop_def.mode = FormalParameterModeType.IN

            ea_node = field_node.find(
                'xpdl:ExtendedAttributes/xpdl:ExtendedAttribute',
                namespaces=NS_MAP)
            if (ea_node is not None):
                ea_name = ea_node.get('Name')
                ea_value = ea_node.get('Value')
                if (ea_name and ea_name.lower() == 'catalog'):
                    prop_def.catalog = ea_value

            prop_def.save()

            flow_def.property_definition_set.add(prop_def)
            flow_def.save()

    @classmethod
    def update_flow_definition_status(cls, flow_definition, status):
        """
        Updates the status of the flow definition. 
        """
        if (status == FlowDefinitionStatusType.UNDER_TEST):
            flow_definition.status = status
        elif (status == FlowDefinitionStatusType.UNDER_REVISION):
            flow_definition.status = status
        elif (status == FlowDefinitionStatusType.RELEASED):
            flow_definition.status = status
        elif (status == FlowDefinitionStatusType.PHASED_OUT):
            flow_definition.status = status
        elif (status == FlowDefinitionStatusType.CANCELLED):
            flow_definition.status = status
        else:
            raise InvalidStatusException(
                _(__name__ + '.exceptions.invalid_flow_definition_status'))
        flow_definition.save()

    @classmethod
    def delete_cases_by_flow_definition(cls, flow_definition):
        """ 
        Deletes all cases by flow definition
        """
        for flow_case in flow_definition.flow_case_set.select_related().all():
            for user_notification_option in flow_case.user_notification_option_set.select_related(
            ).all():
                user_notification_option.delete()
            for flow_property in flow_case.property_set.select_related().all():
                flow_property.delete()
            for doc in flow_case.document_set.select_related().all():
                doc.delete()
            for note in flow_case.note_set.select_related().all():
                note.delete()
            for status in flow_case.source.status_set.select_related().all():
                status.delete()
            for activity in flow_case.activity_set.select_related().all():
                for log in activity.activity_log_set.select_related().all():
                    log.delete()
                activity.delete()

            flow_case.delete()

    @classmethod
    def delete_package_by_package_id_and_version(cls, package_id,
                                                 package_version):
        """
        Deletes a package by package id and package version
        
        """
        for flow_package in FlowPackage.objects.filter(
                package_id=package_id).filter(
                    package_version=package_version).all():
            for flow_definition in flow_package.flow_definition_set.select_related(
            ).all():
                for flow_property in flow_definition.property_definition_set.select_related(
                ).all():
                    flow_property.delete()
                for transition in flow_definition.transition_definition_set.select_related(
                ).all():
                    transition.delete()

                for activity in flow_definition.activity_definition_set.select_related(
                ).all():
                    for activity_application in activity.activity_application_definition_set.select_related(
                    ).all():
                        for activity_application_param in activity_application.parameter_definition_set.select_related(
                        ).all():
                            activity_application_param.delete()
                        activity_application.delete()
                    for form in activity.form_set.select_related().all():
                        for param in form.parameter_set.select_related().all():
                            param.delete()
                        form.delete()
                    for validation in activity.validation_set.select_related(
                    ).all():
                        validation.delete()
                    for extra_tab in activity.extra_tab_set.select_related(
                    ).all():
                        for param in extra_tab.parameter_set.select_related(
                        ).all():
                            param.delete()
                        extra_tab.delete()
                    for action in activity.action_definition_set.select_related(
                    ).all():
                        for param in action.parameter_set.select_related().all(
                        ):
                            param.delete()
                        action.delete()
                    activity.delete()

                for participant in flow_definition.participant_definition_set.select_related(
                ).all():
                    participant.delete()

                for application in flow_definition.application_definition_set.select_related(
                ).all():
                    for application_parameter in application.parameter_definition_set.select_related(
                    ).all():
                        application_parameter.delete()
                    application.delete()
                flow_definition.delete()
            flow_package.delete()

    def update_flow_definition_time_estimation(self, flow_def):
        """
        Updates the definition's time estimation based on the values stored on the Activity Definition Records. 
        Assumes all times in the base unit. 
        """
        waiting_time = 0
        working_time = 0

        for activity_def in flow_def.activity_definition_set.select_related(
        ).all():
            waiting_time = waiting_time + activity_def.waiting_time
            working_time = working_time + activity_def.working_time

        flow_def.waiting_time = waiting_time
        flow_def.working_time = working_time
        flow_def.duration = waiting_time + working_time
        flow_def.save()
        return flow_def

    @classmethod
    def update_activity_definition_time_estimation(cls, flow_def, method=None):
        if isinstance(str, method):
            method = TimeEstimationMethodType.to_enum(method)
        if method is None:
            method = TimeEstimationMethodType.to_enum(
                SystemParameter.find_one(
                    "FLOW_ACTIVITY_DEFINITION_TIME_ESTIMATION_METHOD",
                    FieldDataType.STRING,
                    TimeEstimationMethodType.AVERAGE.value))
        if method is None:
            raise ValueError(
                _(__name__ +
                  ".exceptions.invalid_time_estimation_method_type_especified")
            )

        waiting_time = 0
        working_time = 0

        for activity_def in flow_def.activity_definition_set.select_related():
            waiting_time = waiting_time + FlowActivity.find_average_waiting_time(
                activity_def)
            working_time = working_time + FlowActivity.find_average_waiting_time(
                activity_def)

        flow_def.working_time = working_time
        flow_def.waiting_time = waiting_time
        flow_def.duration = waiting_time + working_time

        flow_def.save()
        return flow_def
