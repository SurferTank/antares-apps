'''
Created on Jul 22, 2016

@author: leobelen
'''
import logging

from django.utils.translation import gettext as _

from ..models import ConceptType


logger = logging.getLogger(__name__)


class ConceptTypeConsole(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        pass

    @staticmethod
    def process_commands(params, html=False):
        message = ""
        if ('create' in params):
            message += ConceptTypeConsole._create_concept_type(params, html)
        elif ('help' in params):
            message += "We may say that the concept type help will show up here"
        elif ('list' in params):
            message += ConceptTypeConsole._list_concept_types(params, html)
        elif ('describe' in params):
            message += ConceptTypeConsole._describe_concept_type(params, html)
        elif ('delete' in params):
            message += ConceptTypeConsole._delete_concept_type(params, html)
        else:
            message += _(__name__ + ".console.dont_now_command")

        return message

    @staticmethod
    def _create_concept_type(params, html=False):
        return _(__name__ + ".console.not_implemented_yet")

    @staticmethod
    def _list_concept_types(params, html=False):
        return _(__name__ + ".console.not_implemented_yet")

    @staticmethod
    def _describe_concept_type(params, html=False):
        return _(__name__ + ".console.not_implemented_yet")

    @staticmethod
    def _delete_concept_type(params, html=False):
        if ('withid' in params):
            try:
                concept_type = ConceptType.find_one(params['withid'])
                if (concept_type is None):
                    return _(__name__ + ".console.concept_type_was_not_found")
            except Exception:
                return _(__name__ + ".console.concept_type_error")
        else:
            return _(__name__ + ".console.missing_parameter %(parameter)s ") % \
                {'parameter': 'withid'}
        if (concept_type.objects.get_queryset_descendants(
                include_self=False).all()):
            return _(__name__ + ".console.delete.deletion_only_works_on_leafs %(concept_type_id)s ") % \
                {'concept_type_id': params['withid']}
        else:
            concept_type.delete()
            return _(__name__ + ".console.delete.successful_deletion")
