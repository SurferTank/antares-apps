'''
Created on Jul 22, 2016

@author: leobelen
'''
from antares.apps.client.constants import ClientStatusType
from antares.apps.client.models.client import Client
from antares.apps.core.constants import FieldDataType, TimeUnitType
from antares.apps.core.manager.period_manager import PeriodManager
from antares.apps.core.models import SystemParameter
from builtins import classmethod
import logging

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.utils.translation import ugettext as _
import js2py

from ..constants import ObligationStatusType, ObligationType
from ..models import ClientObligation
from ..models import ObligationRule, ObligationVector


logger = logging.getLogger(__name__)


class ObligationManager(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        pass

    @classmethod
    def _evaluate_boolean_condition(cls, condition, client, form_definition):
        """
        Evaluates the condition with an unified set of parameters.
        :param: client - the client
        :param: formDefinition - the form definition, if needed
        :return: a bindings object loaded with the passed objects
        """
        if condition:
            context = js2py.EvalJs({
                'client': client,
                'form_definiton': form_definition
            })
            context.execute('return_value = ' + condition)
            if (hasattr(context, 'return_value')):
                return context.return_value
            else:
                return False
        return True

    @classmethod
    def _evaluate_value(cls, condition, client, form_definition):
        """
        Evaluates the condition with an unified set of parameters to obtain a value.
        :param: client - the client
        :param: formDefinition - the form definition, if needed
        :return: a bindings object loaded with the passed objects
        """
        if condition:
            context = js2py.EvalJs({
                'client': client,
                'form_definiton': form_definition
            })
            return context.execute(condition)
        else:
            return True

    @classmethod
    def _get_obligations_to_process(cls, client, concept_type, form_definition,
                                    start_date, end_date):
        obligation_list = []
        if (concept_type is not None):
            for obligation_rule in ObligationRule.find_active_by_concept_type(
                    concept_type):
                if (ObligationManager._evaluate_boolean_condition(
                        obligation_rule.obligation_condition, client,
                        form_definition) is not False):
                    if (obligation_rule.init_date_expression):
                        eval_start_date = ObligationManager._evaluate_value(
                            obligation_rule.init_date_expression, client,
                            form_definition)
                        if (eval_start_date is not None):
                            start_date = eval_start_date
                    if (obligation_rule.end_date_expression):
                        eval_end_date = ObligationManager._evaluate_value(
                            obligation_rule.end_date_expression, client,
                            form_definition)
                        if (eval_end_date is not None):
                            end_date = eval_end_date
                    obligation_row = {}
                    obligation_row['client'] = client
                    obligation_row['concept_type'] = concept_type
                    obligation_row[
                        'account_type'] = obligation_rule.account_type
                    obligation_row['obligation_rule'] = obligation_rule
                    if (form_definition is not None):
                        obligation_row['form_definition'] = form_definition
                    else:
                        obligation_row['form_definition'] = None
                    if (start_date is not None):
                        obligation_row['start_date'] = start_date
                    else:
                        obligation_row['start_date'] = timezone.now()
                    if (end_date is not None):
                        obligation_row['end_date'] = end_date
                    else:
                        obligation_row['end_date'] = None
                    obligation_list.append(obligation_row)

        elif (form_definition is not None):
            raise NotImplementedError
        return obligation_list

    @classmethod
    def _check_or_create_client_obligation(cls, obligation_row):
        """
        Verifies and creates -if needed- the client obligation records, used to calculate the obligations vector.
        """
        client_obligation_list = ClientObligation.find_by_client_and_concept_type(
            obligation_row['client'],
            obligation_row['obligation_rule'].concept_type)
        if (len(client_obligation_list) == 0):
            client_obligation = ClientObligation()
            client_obligation.client = obligation_row['client']
            client_obligation.obligation_rule = obligation_row[
                'obligation_rule']
            client_obligation.concept_type = obligation_row['concept_type']
            client_obligation.form_definition = obligation_row[
                'form_definition']
            client_obligation.start_date = obligation_row['start_date']
            client_obligation.account_type = obligation_row['account_type']
            client_obligation.end_date = obligation_row['end_date']
            client_obligation.save()

            ObligationManager.update_obligation_status(client_obligation)
        else:
            for client_obligation in client_obligation_list:
                ObligationManager.update_obligation_status(client_obligation)

    @classmethod
    def update_obligation_status(cls, client_obligation):
        """
        This method simply calculates the periods and their due dates and
        verifies and updates the obligation status records accordingly.
        """
        period_list = PeriodManager.find_period_list_by_client_obligation(
            client_obligation, timezone.now())
        for period in period_list:
            obligation_status = ObligationVector.find_one_by_COPAD(
                client_obligation.client, client_obligation.concept_type,
                period, client_obligation.account_type,
                client_obligation.base_document)
            if (obligation_status is None or obligation_status.status == ObligationStatusType.CANCELLED):
                due_date = PeriodManager.calculate_date_from_period(
                    client_obligation.obligation_rule.base_date, period,
                    TimeUnitType.to_enum(
                        client_obligation.obligation_rule.time_unit_type),
                    client_obligation.obligation_rule.saturdays_are_holiday,
                    client_obligation.obligation_rule.sundays_are_holiday,
                    client_obligation.obligation_rule.consider_holidays)
                ObligationVector.find_or_create_status(
                    client_obligation.client, client_obligation.concept_type,
                    period, client_obligation.account_type,
                    client_obligation.base_document, client_obligation,
                    ObligationType.to_enum(
                        client_obligation.obligation_rule.obligation_type),
                    due_date)
            elif obligation_status.status == ObligationStatusType.PENDING:
                """ lets update the outdated if they need to be updated """
                if obligation_status.compliance_date is not None:
                    obligation_status.status = ObligationStatusType.COMPLIANT
                    obligation_status.save() 
                elif obligation_status.due_date < timezone.now():
                    obligation_status.status = ObligationStatusType.LATE
                    obligation_status.save()
                
            else:
                logger.info(
                    _("antares.apps.obligation.manager.obligation_manager.obligation_status_found_nothing_to_do"
                      ))

    @classmethod
    def process_obligations(cls, client, concept_type, form_def, when,
                            start_date, end_date):
        """
        This method processes the obligation rules to create obligations that
        will be enforced on the clients.

        <h1>Steps to get this accomplished</h1>
         <ul>
             <li>Get a list of all Obligation rules applicable, and process the
                conditions to discard the incorrect ones.</li>
             <li>Verify and create/update - if needed - the client obligation records</li>
             <li>Create the missing obligation status records</li>
         </ul>
        """
        for obligation in cls._get_obligations_to_process(
                client, concept_type, form_def, start_date, end_date):
            ObligationManager._check_or_create_client_obligation(obligation)

    @classmethod
    def process_obligations_by_client(cls, client, when):
        ObligationManager.process_obligations(client, None, when, None, None)

    @classmethod
    def get_form_definition_by_concept_type_and_period(period, concept_type):
        return
