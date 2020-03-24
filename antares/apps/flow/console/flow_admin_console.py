'''
Created on Jul 5, 2016

@author: leobelen
'''
from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
from antares.apps.flow.constants import FlowActivityStatusType
from antares.apps.flow.models.operation import FlowCase, FlowActivity
from antares.apps.subscription.manager import SubscriptionManager
from antares.apps.user.models import User
import logging
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from ..constants import FlowDefinitionStatusType, TimeEstimationMethodType
from ..manager import FlowAdminManager
from ..models import FlowPackage


logger = logging.getLogger(__name__)


class FlowAdminConsole(object):
    '''
    classdocs
    '''

    @classmethod
    def process_commands(cls, params, html=False):
        message = ""
        if ('loadxpdl' in params):
            message += FlowAdminConsole._load_xpdl(params, html)
        elif ('packagelist' in params):
            message += FlowAdminConsole._get_package_list(params, html)
        elif ('definitionlist' in params):
            message += FlowAdminConsole._get_definition_list(params, html)
        elif ('deletepackage' in params):
            message += FlowAdminConsole._delete_package(params, html)
        elif ('deletecases' in params):
            message += FlowAdminConsole._delete_cases(params, html)
        elif ('setdefinitionstatus' in params):
            message += FlowAdminConsole._set_definition_status(params, html)
        elif ('listactivities' in params):
            message += FlowAdminConsole._list_activities(params, html)
        elif ('reassignactivity' in params):
            message += FlowAdminConsole._reassign_activity(params, html)
        elif ('updateestimation' in params):
            message += FlowAdminConsole._update_estimation(params, html)

        elif ('help' in params):
            message += "We may say that the flow help will show up here"
        else:
            message += _(__name__ + ".console.dont_now_command")

        return message

    @classmethod
    def _get_package_list(cls, params, html=False):
        package_list = FlowPackage.find_all()
        if (len(package_list) == 0):
            return _(__name__ + ".console.no_packages_found")
        if (html == True):
            result = "<table width=\"100%\"><tr><td><b>" + \
                _(__name__ + ".console.package_id") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.package_version") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.package_name") + \
                "</b></td></tr>"
            for package in package_list:
                result += "<tr><td>" + package.package_id + "</td>"
                if (package.package_version):
                    result += "<td>" + package.package_version + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if (package.package_name):
                    result += "<td>" + package.package_name + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                result += '</tr>'
            result += '</table>'
            return result
        else:
            raise NotImplementedError

    @classmethod
    def _get_definition_list(cls, params, html=False):
        if ('withpackageid' in params):
            package_id = params['withpackageid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageid'}
        if ('withpackageversion' in params):
            package_version = params['withpackageversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageversion'}
        package = FlowPackage.find_one_by_package_id_and_package_version(
            package_id, package_version)
        if (package is None):
            return _(__name__ + ".console.package_does_not_exist")
        flow_definition_list = package.flow_definition_set.select_related(
        ).all()
        if (len(flow_definition_list) == 0):
            return _(__name__ + ".console.package_has_no_flows")
        if (html == True):
            result = "<table width=\"100%\"><tr><td><b>" + \
                _(__name__ + ".console.flow_id") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.flow_version") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.flow_name") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.flow_description") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.flow_status") + \
                "</b></td></tr>"
            for flow_definition in flow_definition_list:
                result += "<tr><td>" + flow_definition.flow_id + "</td>"
                if (flow_definition.flow_version):
                    result += "<td>" + flow_definition.flow_version + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if (flow_definition.flow_name):
                    result += "<td>" + flow_definition.flow_name + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if (flow_definition.description):
                    result += "<td>" + flow_definition.description + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if (flow_definition.status
                        and FlowDefinitionStatusType.to_enum(
                            flow_definition.status) is not None):
                    result += "<td>" + str(flow_definition.status) + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                result += '</tr>'
            result += '</table>'
            return result
        else:
            raise NotImplementedError

    @classmethod
    def _delete_package(cls, params, html=False):
        if ('withpackageid' in params):
            package_id = params['withpackageid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageid'}
        if ('withpackageversion' in params):
            package_version = params['withpackageversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageversion'}
        package = FlowPackage.find_one_by_package_id_and_package_version(
            package_id, package_version)
        if (package is None):
            return _(__name__ + ".console.package_does_not_exist")

        FlowAdminManager.delete_package_by_package_id_and_version(
            package_id, package_version)

        return _(__name__ + ".console.package_deleted_sucessfully")

    @classmethod
    def _delete_cases(cls, params, html=False):
        if ('withpackageid' in params):
            package_id = params['withpackageid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageid'}
        if ('withpackageversion' in params):
            package_version = params['withpackageversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageversion'}

        package = FlowPackage.find_one_by_package_id_and_package_version(
            package_id, package_version)
        if (package is None):
            return _(__name__ + ".console.package_not_found")
        if ('withdefinitionid' in params):
            flow_definition_id = params['withdefinitionid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdefinitionid'}
        if ('withdefinitionversion' in params):
            flow_definition_version = params['withdefinitionversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdefinitionversion'}
        try:
            flow_definition = package.flow_definition_set.select_related().get(
                flow_id=flow_definition_id,
                flow_version=flow_definition_version)
        except ObjectDoesNotExist:
            return _(__name__ + ".console.flow_does_not_exist_in_package")

        FlowAdminManager.delete_cases_by_flow_definition(flow_definition)

        return _(__name__ + ".cases_sucessfully_deleted")

    @classmethod
    def _set_definition_status(cls, params, html=False):
        if ('withpackageid' in params):
            package_id = params['withpackageid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageid'}
        if ('withpackageversion' in params):
            package_version = params['withpackageversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageversion'}

        package = FlowPackage.find_one_by_package_id_and_package_version(
            package_id, package_version)
        if ('withdefinitionid' in params):
            flow_definition_id = params['withdefinitionid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdefinitionid'}
        if ('withdefinitionversion' in params):
            flow_definition_version = params['withdefinitionversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdefinitionversion'}
        try:
            flow_definition = package.flow_definition_set.select_related().get(
                flow_id=flow_definition_id,
                flow_version=flow_definition_version)
        except ObjectDoesNotExist:
            return _(__name__ + ".console.flow_does_not_exist_in_package")

        if ('withstatus' in params and FlowDefinitionStatusType.to_enum(
                params['withstatus']) is not None):
            flow_status = FlowDefinitionStatusType.to_enum(
                params['withstatus'])
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withstatus'}

        FlowAdminManager.update_flow_definition_status(flow_definition,
                                                       flow_status)
        if (flow_status == FlowDefinitionStatusType.UNDER_TEST):
            SubscriptionManager.subscribe_flow_definition(flow_definition)
        elif (flow_status == FlowDefinitionStatusType.UNDER_REVISION):
            SubscriptionManager.unsubscribe_flow_definition(flow_definition)
        elif (flow_status == FlowDefinitionStatusType.RELEASED):
            SubscriptionManager.subscribe_flow_definition(flow_definition)
        elif (flow_status == FlowDefinitionStatusType.PHASED_OUT):
            SubscriptionManager.unsubscribe_flow_definition(flow_definition)
        elif (flow_status == FlowDefinitionStatusType.CANCELLED):
            SubscriptionManager.unsubscribe_flow_definition(flow_definition)

        return _(__name__ + ".console.flow_status_was_changed_successfully")

    @classmethod
    def _load_xpdl(cls, params, html=False):
        if ('withfile' in params):
            manager = FlowAdminManager(xpdl_file=params['withfile'])
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withfile'}

        manager.load_xpdl()

        return _(__name__ + ".console.load_xpdl_sucess")

    @classmethod
    def _list_activities(cls, params, html):
        date_format_string = UserParameter.find_one(
            get_request().user, 'CORE_TEMPLATE_DATE_TIME_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d %H:%M')
        if ('withcaseid' in params):
            flow_case = FlowCase.find_one(UUID(params['withcaseid']))
        elif ('withcode' in params):
            flow_case = FlowCase.find_one_by_hrn_code(params['withcode'])
        else:
            return _(
                __name__ + 
                ".console.either_withcaseid_or_withcode_parameters_have_to_be_defined"
            )
        if flow_case is None:
            return _(__name__ + ".console.no_case_was_found")
        if (html == True):
            result = "<table width=\"90%\"><tr><td><b>" + \
                _(__name__ + ".console.activity_list.activity_code") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.activity_list.status") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.activity_list.creation_date") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.activity_list.start_date") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.activity_list.end_date") + \
                "</b></td><td><b>" + \
                _(__name__ + ".console.activity_list.performer") + \
                "</b></td></tr>"
            for activity in flow_case.activity_set.select_related().order_by(
                    'creation_date').all():
                result += "<tr>"
                if activity.hrn_code:
                    result += "<td>" + activity.hrn_code + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if activity.status:
                    result += "<td>" + activity.status.label + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if activity.creation_date:
                    result += "<td>" + activity.creation_date.strftime(
                        date_format_string) + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if activity.start_date:
                    result += "<td>" + activity.start_date.strftime(
                        date_format_string) + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if activity.completion_date:
                    result += "<td>" + activity.completion_date.strftime(
                        date_format_string) + "</td>"
                else:
                    result += "<td>&nbsp;</td>"
                if activity.performer:
                    try:
                        if activity.performer.client and activity.performer.client.full_name:
                            result += "<td>" + activity.performer.client.full_name + " (" + activity.performer.username + ")</td>"
                        else:
                            result += "<td>" + activity.performer.username + '</td>'
                    except:
                        result += "<td>" + activity.performer.username + '</td>'
                else:
                    result += "<td>&nbsp;</td>"
                result += '</tr>'

            result += '</table>'

            return result

    @classmethod
    def _reassign_activity(cls, params, html):
        if 'withcode' in params:
            flow_activity = FlowActivity.find_one_by_hrn_code(
                params['withcode'])
            if flow_activity is None:
                return _(__name__ + ".console.no_activity_was_found")
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withcode'}

        if 'withusername' in params:
            performer = User.find_one_by_username(params['withusername'])
            if performer is None:
                return _(__name__ + ".console.no_user_was_found")

        if flow_activity.status in (FlowActivityStatusType.CANCELLED,
                                    FlowActivityStatusType.COMPLETED):
            return _(__name__ + 
                     ".activities_finalized_or_cancelled_cannot_be_reassigned")

        flow_activity.performer = performer
        flow_activity.save()

        return _(__name__ + 
                 ".activity_reassigned_to {activity} {username}").format(
                     activity=flow_activity.hrn_code,
                     username=performer.username)

    @classmethod
    def _update_estimation(cls, params, html):
        if ('withpackageid' in params):
            package_id = params['withpackageid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageid'}
        if ('withpackageversion' in params):
            package_version = params['withpackageversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withpackageversion'}

        package = FlowPackage.find_one_by_package_id_and_package_version(
            package_id, package_version)
        if ('withdefinitionid' in params):
            flow_definition_id = params['withdefinitionid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdefinitionid'}
        if ('withdefinitionversion' in params):
            flow_definition_version = params['withdefinitionversion']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdefinitionversion'}
        try:
            flow_definition = package.flow_definition_set.select_related().get(
                flow_id=flow_definition_id,
                flow_version=flow_definition_version)
        except ObjectDoesNotExist:
            return _(__name__ + ".console.flow_does_not_exist_in_package")

        FlowAdminManager.update_flow_definition_time_estimation(
            flow_definition, TimeEstimationMethodType.AVERAGE)

        return _(__name__ + ".console.estimations_successfully_updated")
