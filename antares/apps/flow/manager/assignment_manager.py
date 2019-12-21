'''
Created on Jul 13, 2016

@author: leobelen
'''
import logging
import random

from antares.apps.user.models import User

from ..enums  import AssignmentStrategyType

logger = logging.getLogger(__name__)


class AssignmentManager(object):
    '''
    classdocs
    '''

    @staticmethod
    def get_activity_performer(activity):
        """
        
        """
        strategy = activity.activity_definition.assignment_strategy
        participant_definition_set = activity.activity_definition.\
            participant_definition_set.select_related()
        if len(participant_definition_set) == 0 or strategy is None:
            return User.get_system_user()
        if strategy == AssignmentStrategyType.RANDOM:
            return AssignmentManager._get_random_performer(activity)
        if strategy == AssignmentStrategyType.DIRTY_RANDOM:
            return AssignmentManager._get_dirty_random_performer(activity)
        if strategy == AssignmentStrategyType.ACTIVITY:
            return AssignmentManager._get_activity_performer(activity)
        if strategy == AssignmentStrategyType.PROPERTY:
            return AssignmentManager._get_property_performer(activity)
        if strategy == AssignmentStrategyType.WORKLOAD:
            return AssignmentManager._get_workload_performer(activity)
        if strategy == AssignmentStrategyType.NONE:
            # none means the system here
            return User.get_system_user()

        return User.get_system_user()

    @classmethod
    def _get_random_performer(cls, activity):
        """ 
        Gets the full list of participants and picks one in a random fashion 
        """
        participants = cls._find_participants_by_activity(activity)
        if len(participants) == 0:
            return User.get_system_user()
        else:
            #TODO: this should fail, but for now it will return the system user.
            return random.choice(participants)

    @classmethod
    def _find_participants_by_activity(cls, activity):
        """
        """
        participants = []
        for participant in activity.activity_definition.participant_definition_set.select_related(
        ):
            participants.extend(
                User.find_by_user_id_org_unit_role(participant.user_id,
                                                   participant.org_unit,
                                                   participant.role))
        return participants

    @classmethod
    def _get_dirty_random_performer(cls, activity):
        """
        """
        pass

    @classmethod
    def _get_activity_performer(cls, activity):
        """
        """
        pass

    @classmethod
    def _get_property_performer(cls, activity):
        """
        """
        pass

    @classmethod
    def _get_workload_performer(cls, activity):
        """
        """
        pass
