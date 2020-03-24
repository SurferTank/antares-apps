'''
Created on 30/7/2016

@author: leobelen
'''
from antares.apps.core.middleware.request import get_request
import logging

from django.utils.translation import ugettext as _

from ..constants import ClientRelationType
from ..models import Client
from ..models import ClientUserRelation


logger = logging.getLogger(__name__)


class ClientUserRelationConsole(object):
    '''
    classdocs
    '''

    @staticmethod
    def process_commands(params, html=False):
        message = ""
        if ('list' in params):
            message += ClientUserRelationConsole._list_client_relations(
                params, html)
        elif ('help' in params):
            message += "We may say that the client user relation's help will show up here"
        elif ('getcurrentclient' in params):
            message += ClientUserRelationConsole._get_current_client(
                params, html)
        elif ('setclient' in params):
            message += ClientUserRelationConsole._set_client(params, html)

        else:
            message += _(__name__ + ".console.dont_now_command")

        return message

    @staticmethod
    def _list_client_relations(params, html):
        client_relation_list = ClientUserRelation.get_child_client_list(False)
        if (len(client_relation_list) == 0):
            return _(__name__ + 
                     ".console.the_current_user_has_no_clients_associated")

        result = "<table width=\"100%\"><tr><td>" + \
                 "<b>" + _(__name__ + ".tables.client") + \
                 "</b></td><td>" + \
                 "<b>" + _(__name__ + ".tables.relation_type") + \
                 "</b></td>"
        for client_relation in client_relation_list:
            if (client_relation.child_client.code
                    and client_relation.child_client.full_name):
                result += "<tr><td>" + client_relation.child_client.code + \
                    " - " + client_relation.child_client.full_name + "</td>"
            elif (client_relation.child_client.code):
                result += "<tr><td>" + client_relation.child_client.code + "</td>"
            else:
                result += "<tr><td>" + str(
                    client_relation.child_client.id) + "</td>"
            if (client_relation.relation_type):
                result += "<td>" + ClientRelationType.to_enum(
                    client_relation.relation_type).get_label() + "</td>"

            result += '</tr>'

        result += '</table>'
        return result

    @staticmethod
    def _get_current_client(params, html):
        current_client = get_request().user.get_on_behalf_client()
        if (current_client is not None):
            return _(__name__ + ".current_client_is %(client_name)s") % \
                {'client_name': current_client.code + 
                    ' - ' + current_client.full_name}

    @staticmethod
    def _set_client(params, html):
        """
         Sets a client to act on behalf of
        """
        # TODO: God role (that is, a role to allow impersonation of any client)
        # is not implemented yet.
        if ('withclientcode' in params):
            client = Client.find_one_by_code(params['withclientcode'])
            if (client is None):
                return _(__name__ + ".no_client_found_by_id %(client_id)s") % \
                    {'client_id': params['withclientcode']}
            get_request().user.set_on_behalf_client(client)
            return _(__name__ + ".switched_to_specified_client")
        elif ('withself' in params):
            get_request().user.set_on_behalf_client(get_request().user.client)
            return _(__name__ + ".switched_to_own_client")
        else:
            return _(__name__ + ".missing_parameter %(parameter)s ") % \
                {'parameter': 'withid'}
