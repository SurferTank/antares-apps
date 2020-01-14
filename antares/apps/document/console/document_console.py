'''
Created on Jun 17, 2016

@author: leobelen
'''
import logging

from dateutil import parser as dateparser
from django.utils.translation import ugettext as _

from antares.apps.core.constants import FieldDataType

from ..types import Document


logger = logging.getLogger(__name__)


class DocumentConsole(object):
    """
    Services to process the Remote Console inteface

    """

    def __init__(self, params):
        pass

    @staticmethod
    def process_commands(params, html=False):
        message = ""
        if ('create' in params):
            message += DocumentConsole.create_document(params, html)
        elif ('help' in params):
            message += "We may say that the help will show up here"
        elif ('listfields' in params):
            message += DocumentConsole.list_fields(params, html)
        elif ('listheaderfields' in params):
            message += DocumentConsole.list_header_fields(params, html)
        elif ('setfield' in params):
            message += DocumentConsole.set_field(params, html)
        elif ('setheaderfield' in params):
            message += DocumentConsole.set_header_field(params, html)
        elif ('setaccountinformation' in params):
            message += DocumentConsole.set_account_information(params, html)
        else:
            message += _(__name__ + ".console.dont_now_command")

        return message

    @staticmethod
    def create_document(params, html=False):
        if ('withformid' in params):
            form_id = params['withformid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withformid'}

        document = Document(form_id=form_id)
        return _(__name__ + ".console.create_document_success %(document_id)s ") % \
            {'document_id': str(document.document_id)}

    @staticmethod
    def set_field(params, html=False):
        if ('withdocumentid' in params):
            try:
                document = Document(document_id=params['withdocumentid'])
            except Exception:
                return _(__name__ + ".console.document_error")
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdocumentid'}
        if ('withfieldid' in params):
            field_id = params['withfieldid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withfieldid'}
        if ('withvalue' in params):
            value = params['withvalue']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withvalue'}
        document.set_field_value(field_id, value)
        document.save()

        return _(__name__ + ".console.field_value_saved")

    @staticmethod
    def list_fields(params, html=False):
        if ('withdocumentid' in params):
            try:
                document = Document(document_id=params['withdocumentid'])
            except Exception as e:
                return _(__name__ + ".console.document_error")
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdocumentid'}
        result = "<table width=\"100%\"><tr><td " + \
                 "width=\"20%\"><b>" + _(__name__ + ".console.tables.field_id") + \
                 "</b></td><td width=\"20%\"><b>" + \
                 _(__name__ + ".console.tables.field_type") + \
                 "</b></td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.value") + \
                 "</b></td></tr>"

        fields = document.get_field_dict()
        for key, value in fields.items():
            datatype = document.get_field_data_type(key)
            result += "<tr><td>" + key + "</td><td>" + \
                str(datatype) + "</td><td>"
            if (value is not None):
                if (datatype == FieldDataType.BOOLEAN):
                    if (value == True):
                        result += _('Yes')
                    else:
                        result += _('No')
                elif (datatype == FieldDataType.DATE):
                    result += value.isodate()
                elif (datatype == FieldDataType.FLOAT):
                    result += str(value)
                elif (datatype == FieldDataType.INTEGER):
                    result += str(value)
                elif (datatype == FieldDataType.UUID):
                    result += str(value)
                else:
                    result += value
            else:
                result += ' '

            result += "</td></tr>"
        result += "</tr></table>"
        return result

    @staticmethod
    def list_header_fields(params, html=False):
        if ('withdocumentid' in params):
            try:
                document = Document(document_id=params['withdocumentid'])
            except Exception as e:
                return _(__name__ + ".console.document_error")
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdocumentid'}
        result = "<table width=\"100%\"><tr><td " + \
                 "width=\"20%\"><b>" + _(__name__ + ".console.tables.field_id") + \
                 "</b></td><td width=\"60%\"><b>" + _(__name__ + ".console.tables.value") + \
                 "</b></td></tr>"

        fields = document.get_header_field_dict(True)
        if ('save_date' in fields):
            result += "<tr><td>" + 'save_date' + "</td><td>"

            if (fields['save_date'] is not None):
                result += fields['save_date'].isoformat()
            else:
                result += ' '
            result += "</td></tr>"
        if ('secondary_client' in fields):
            result += "<tr><td>" + 'secondary_client' + "</td><td>"

            if (fields['secondary_client'] is not None):
                result += str(fields['secondary_client'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('hrn_string' in fields):
            result += "<tr><td>" + 'hrn_string' + "</td><td>"

            if (fields['hrn_string'] is not None):
                result += fields['hrn_string']
            else:
                result += ' '
            result += "</td></tr>"

        if ('hrn_title' in fields):
            result += "<tr><td>" + 'hrn_title' + "</td><td>"

            if (fields['hrn_title'] is not None):
                result += fields['hrn_title']
            else:
                result += ' '
            result += "</td></tr>"

        if ('concept_type' in fields):
            result += "<tr><td>" + 'concept_type' + "</td><td>"

            if (fields['concept_type'] is not None):
                result += str(fields['concept_type'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('delete_case' in fields):
            result += "<tr><td>" + 'delete_case' + "</td><td>"

            if (fields['delete_case'] is not None):
                result += str(fields['delete_case'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('status' in fields):
            result += "<tr><td>" + 'status' + "</td><td>"

            if (fields['status'] is not None):
                result += str(fields['status'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('association_type' in fields):
            result += "<tr><td>" + 'association_type' + "</td><td>"

            if (fields['association_type'] is not None):
                result += str(fields['association_type'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('associated_to' in fields):
            result += "<tr><td>" + 'associated_to' + "</td><td>"

            if (fields['associated_to'] is not None):
                result += str(fields['associated_to'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('related_case' in fields):
            result += "<tr><td>" + 'related_case' + "</td><td>"

            if (fields['related_case'] is not None):
                result += str(fields['related_case'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('client' in fields):
            result += "<tr><td>" + 'client' + "</td><td>"

            if (fields['client'] is not None):
                result += str(fields['client'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('creation_date' in fields):
            result += "<tr><td>" + 'creation_date' + "</td><td>"

            if (fields['creation_date'] is not None):
                result += fields['creation_date'].isoformat()
            else:
                result += ' '
            result += "</td></tr>"

        if ('draft_date' in fields):
            result += "<tr><td>" + 'draft_date' + "</td><td>"

            if (fields['draft_date'] is not None):
                result += fields['draft_date'].isoformat()
            else:
                result += ' '
            result += "</td></tr>"

        if ('author' in fields):
            result += "<tr><td>" + 'author' + "</td><td>"

            if (fields['author'] is not None):
                result += fields['author'].isoformat()
            else:
                result += ' '
            result += "</td></tr>"

        if ('active_version' in fields):
            result += "<tr><td>" + 'active_version' + "</td><td>"

            if (fields['active_version'] == True):
                result += _("Yes")
            else:
                result += _("No")
            result += "</td></tr>"

        if ('base_document' in fields):
            result += "<tr><td>" + 'base_document' + "</td><td>"

            if (fields['base_document']):
                result += str(fields['base_document'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('document_version' in fields):
            result += "<tr><td>" + 'document_version' + "</td><td>"

            if (fields['document_version']):
                result += str(fields['document_version'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('period' in fields):
            result += "<tr><td>" + 'period' + "</td><td>"

            if (fields['period']):
                result += str(fields['period'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('hash' in fields):
            result += "<tr><td>" + 'hash' + "</td><td>"

            if (fields['hash']):
                result += str(fields['hash'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('account_type' in fields):
            result += "<tr><td>" + 'account_type' + "</td><td>"

            if (fields['account_type']):
                result += str(fields['account_type'])
            else:
                result += ' '
            result += "</td></tr>"

        if ('origin' in fields):
            result += "<tr><td>" + 'origin' + "</td><td>"

            if (fields['origin']):
                result += str(fields['origin'])
            else:
                result += ' '
            result += "</td></tr>"

        result += "</table>"
        return result

    @staticmethod
    def set_header_field(params, html=False):
        if ('withdocumentid' in params):
            try:
                document = Document(document_id=params['withdocumentid'])
            except Exception as e:
                return _(__name__ + ".console.document_error")
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withdocumentid'}
        if ('withfieldid' in params):
            field_id = params['withfieldid']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withfieldid'}
        if ('withvalue' in params):
            value = params['withvalue']
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withvalue'}
        document.set_header_value(field_id, value)
        document.save()

        return _(__name__ + ".console.header_field_value_saved")

    @staticmethod
    def set_account_information(params, html=False):
        return "Not implemented yet"
