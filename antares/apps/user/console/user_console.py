'''
Created on 16 feb. 2017

@author: leobelen
'''

import logging

from django.utils.translation import ugettext as _

from ..models import User


logger = logging.getLogger(__name__)


class UserConsole(object):
    '''
    classdocs
    '''

    @classmethod
    def process_commands(cls, params, html=False):
        message = ""
        if ('help' in params):
            message += "We may say that the help will show up here"
        elif ('showidbyusername' in params):
            message += cls._show_id_by_login(params, html)
        else:
            message += _(__name__ + ".dont_now_command")

        return message

    @classmethod
    def _show_id_by_login(cls, params, html):
        if ('withusername' in params):
            user = User.find_one_by_user_name(params['withusername'])
        else:
            return _(__name__ + ".missing_parameter {parameter}").format(
                parameter='withusername')
        if user is not None:
            return _(__name__ + ".the_user_id_is {username} {userid}").format(
                username=user.username, userid=user.id)
