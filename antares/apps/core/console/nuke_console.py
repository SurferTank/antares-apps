'''
Created on Jul 22, 2016

@author: leobelen
'''
from antares.apps.document.models import FormDefinition
from antares.apps.flow.manager import FlowAdminManager
from antares.apps.flow.models import FlowDefinition, FlowPackage
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from ..service import NukeService


logger = logging.getLogger(__name__)


class NukeConsole(object):

    @classmethod
    def process_commands(cls, params, html=False):
        message = ""
        if ('deletedocuments' in params):
            message += cls._delete_documents(params, html)
        elif ('help' in params):
            message += "We may say that the nuke help will show up here"
        elif ('deletepackage' in params):
            message += cls._delete_flow_definitions(params, html)
        elif ('deletecases' in params):
            message += cls._delete_cases(params, html)
        else:
            message += _(__name__ + ".console.dont_now_command")

        return message

    @classmethod
    def _delete_documents(cls, params, html=False):
        if 'withformid' in params:
            form_def = FormDefinition.find_one(params['withformid'])
            if form_def is None:
                return _(__name__ + ".console.form_not_found")
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withformid'}

        try:
            NukeService.delete_documents(form_def)
            return _(__name__ + ".messages.all_documents_have_been_deleted")
        except Exception as e:
            return _(__name__ + ".messages.the_documents_could_not_be_deleted")

    @classmethod
    def _delete_flow_definitions(cls, params, html=False):
        if ('withid' in params):
            package = FlowPackage.find_one_by_id(params['withid'])
            package_id = package.package_id
            package_version = package.package_version
        else:
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
