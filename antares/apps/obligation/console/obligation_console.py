'''
Created on Jul 24, 2016

@author: leobelen
'''
import logging

import dateutil.parser
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.client.models import Client
from antares.apps.core.models import ConceptType
from antares.apps.document.models import FormDefinition

from ..constants import ObligationType, ObligationStatusType
from ..manager import ObligationManager
from ..models import ObligationVector

logger = logging.getLogger(__name__)


class ObligationConsole(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        pass

    @classmethod
    def process_commands(cls, params, html=False):
        message = ""
        if ('process' in params):
            message += ObligationConsole.process_obligations(params, html)
        elif ('list' in params):
            message += ObligationConsole.list_obligations(params, html)
        elif ('help' in params):
            message += "We may say that the obligation's help will show up here"

        else:
            message += _(__name__ + ".console.dont_now_command")

        return message

    @classmethod
    def process_obligations(cls, params, html=False):
        if ('withclientid' in params):
            client = Client.find_one(params['withclientid'])
            if (client is None):
                return _(__name__ + ".console.client_was_not_found")
        else:
            if ('withclientcode' in params):
                client = Client.find_one_by_code(params['withclientcode'])
                if (client is None):
                    return _(__name__ + ".console.client_was_not_found")
            else:
                return _(__name__ +
                         ".console.either_client_id_or_code_are_missing")

        if ('withconcepttype' in params):
            concept_type = ConceptType.find_one(params['withconcepttype'])
            if (concept_type is None):
                return _(__name__ + ".console.concept_type_was_not_found")
        else:
            concept_type = None

        if ('withformdefinition' in params):
            form_definition = FormDefinition.find_one(
                params['withformdefinition'])
            if (concept_type is None):
                return _(__name__ + ".console.form_definition_was_not_found")
        else:
            form_definition = None

        if ('when' in params):
            try:
                when_date = dateutil.parser.parse(params['when'])
            except:
                return _(__name__ +
                         ".console.invalid_date_format_for_when_parameter")
        else:
            when_date = timezone.now()

        if ('withstartdate' in params):
            try:
                start_date = dateutil.parser.parse(params['withstartdate'])
            except:
                return _(
                    __name__ +
                    ".console.invalid_date_format_for_withstartdate_parameter")
        else:
            start_date = None

        if ('withenddate' in params):
            try:
                end_date = dateutil.parser.parse(params['withenddate'])
            except:
                return _(
                    __name__ +
                    ".console.invalid_date_format_for_withenddate_parameter")
        else:
            end_date = None

        ObligationManager.process_obligations(client, concept_type,
                                              form_definition, when_date,
                                              start_date, end_date)
        return _(__name__ + ".console.command_sucessfully_run")

    @classmethod
    def list_obligations(cls, params, html=False):
        if ('withclientid' in params):
            client = Client.find_one(params['withclientid'])
            if (client is None):
                return _(__name__ + ".console.client_was_not_found")
        else:
            if ('withclientcode' in params):
                client = Client.find_one_by_code(params['withclientcode'])
                if (client is None):
                    return _(__name__ + ".console.client_was_not_found")
            else:
                return _(__name__ +
                         ".console.either_client_id_or_code_are_missing")

        if ('withobligationtype' in params):
            obligation_type = ObligationType.to_enum(
                params['withobligationtype'])
            if (obligation_type is None):
                return _(__name__ + ".console.obligation_type_was_not_found")
        else:
            obligation_type = None

        if ('withstatus' in params):
            status = ObligationStatusType.to_enum(params['withstatus'])
            if (status is None):
                return _(__name__ + ".console.status_was_not_found")
        else:
            status = None

        if (obligation_type is None and status is None):
            obligation_vector_list = ObligationVector.find_by_client(client)
        elif (obligation_type is not None and status is None):
            obligation_vector_list = ObligationVector.find_by_client_and_obligation_type(
                client, obligation_type)
        elif (obligation_type is not None and status is not None):
            obligation_vector_list = ObligationVector.find_by_client_and_obligation_type_and_status(
                client, obligation_type, status)
        elif (obligation_type is None and status is not None):
            obligation_vector_list = ObligationVector.find_by_client_and_status(
                client, status)

        if (len(obligation_vector_list) == 0):
            return _(__name__ +
                     ".console.no_obligations_found_for_given_parameters")

        result = "<table width=\"100%\"><tr><td " + \
                 "width=\"20%\"><b>" + _(__name__ + ".console.tables.client") + \
                 "</b></td><td width=\"20%\"><b>" + \
                 _(__name__ + ".console.tables.obligation") + \
                 "</b></td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.period") + \
                 "</b></td>" + \
                 "</td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.account_type") + \
                 "</b></td>" + \
                 "</td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.base_document") + \
                 "</b></td>" + \
                 "</td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.status") + \
                 "</b></td>" + \
                 "</td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.due_date") + \
                 "</b></td>" + \
                 "</td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.compliance_date") + \
                 "</b></td>" + \
                 "</tr>"

        for obligation_vector in obligation_vector_list:
            if (obligation_vector.client.code):
                result += "<tr><td>" + obligation_vector.client.code + "</td>"
            else:
                result += "<tr><td>" + str(
                    obligation_vector.client.id) + "</td>"
            if (obligation_vector.concept_type.concept_type_name):
                result += "<td>" + obligation_vector.concept_type.concept_type_name + "</td>"
            else:
                result += "<td>" + str(
                    obligation_vector.concept_type.id) + "</td>"
            result += "<td>" + str(obligation_vector.period) + "</td>"
            if (obligation_vector.account_type.account_type_name):
                result += "<td>" + obligation_vector.account_type.account_type_name + "</td>"
            else:
                result += "<td>" + str(
                    obligation_vector.account_type.id) + "</td>"
            if (obligation_vector.base_document is not None
                    and obligation_vector.base_document.hrn_string):
                result += "<td>" + obligation_vector.base_document.hrn_string + "</td>"
            elif (obligation_vector.base_document is not None):
                result += "<td>" + str(
                    obligation_vector.base_document.id) + "</td>"
            else:
                result += "<td>&nbsp;</td>"
            if (obligation_vector.status is not None
                    and ObligationStatusType.to_enum(
                        obligation_vector.status) is not None):
                result += "<td>" + ObligationStatusType.to_enum(
                    obligation_vector.status).get_label() + "</td>"
            else:
                result += "<td>&nbsp;</td>"
            if (obligation_vector.due_date is not None):
                result += "<td>" + obligation_vector.due_date.isoformat(
                ) + "</td>"
            else:
                result += "<td>&nbsp;</td>"
            if (obligation_vector.compliance_date is not None):
                result += "<td>" + obligation_vector.compliance_date.isoformat(
                ) + "</td>"
            else:
                result += "<td>&nbsp;</td>"
            result += '</tr>'
        result += '</table>'
        return result
