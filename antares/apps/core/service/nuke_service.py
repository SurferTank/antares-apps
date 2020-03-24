'''
Created on Jun 30, 2016

@author: leobelen
'''
from antares.apps.accounting.models import AccountBalance, AccountDocument, AccountTransaction, AccountRule
from antares.apps.document.models import DocumentHeader, DocumentField, IndexedField, DocumentHrn, DocumentTableContent, FormDefinition
from antares.apps.flow.models import PropertyDefinition, TransitionDefinition, ActivityDefinition, ParticipantDefinition, \
    ApplicationDefinition, FlowDefinition, FlowPackage, ActivityApplicationDefinition, ActivityApplicationParameterDefinition, \
    ApplicationParameterDefinition
import logging


class NukeService(object):
    '''
    A service to reset the database during setup
    '''

    logger = logging.getLogger(__name__)

    def __init__(self, params):
        '''
        Constructor
        '''
        pass

    @classmethod
    def delete_all_account_rules(cls):
        NukeService.delete_all_accounts()
        for rule in AccountRule.objects.all():
            rule.delete()

    @classmethod
    def delete_all_accounts(cls):
        for account_document in AccountDocument.objects.all():
            account_document.delete()
        for transaction in AccountTransaction.objects.all():
            transaction.delete()
        for balance in AccountBalance.objects.all():
            balance.delete()

    @classmethod
    def delete_documents(cls, form_definition=None):
        if form_definition is None:
            NukeService.delete_all_accounts()
            for table_content in DocumentTableContent.objects.all():
                table_content.delete()
            for hrn in DocumentHrn.objects.all():
                hrn.delete()
            for indexed_field in IndexedField.objects.all():
                indexed_field.delete()
            for field in DocumentField.objects.all():
                field.delete()
            for document in DocumentHeader.objects.all():
                document.delete()
        else:
            for document_header in DocumentHeader.objects.filter(
                    form_definition=form_definition):
                for table_content in document_header.table_content_set.select_related(
                ).all():
                    table_content.delete()
                for hrn in document_header.document_hrn_set.select_related(
                ).all():
                    hrn.delete()
                for indexed_field in document_header.indexed_field_set.select_related(
                ).all():
                    indexed_field.delete()
                for field in document_header.field_set.select_related().all():
                    field.delete()
                document_header.delete()

    @classmethod
    def delete_all_form_definitions(cls):
        NukeService.delete_all_account_rules()
        for form_def in FormDefinition.objects.all():
            form_def.delete()

    @classmethod
    def reset_document_module(cls):
        NukeService.delete_all_documents()
        NukeService.delete_all_form_definitions()

    @classmethod
    def delete_all_flow_definitions(cls, package_id, package_version):
        for flow_property in PropertyDefinition.objects.all():
            flow_property.delete()
        for transition in TransitionDefinition.objects.all():
            transition.delete()
        for activity_application_param in ActivityApplicationParameterDefinition.objects.all(
        ):
            activity_application_param.delete()
        for activity_application in ActivityApplicationDefinition.objects.all(
        ):
            activity_application.delete()
        for activity in ActivityDefinition.objects.all():
            for form in activity.form_set.select_related().all():
                for param in form.parameter_set.select_related().all():
                    param.delete()
                form.delete()
            for validation in activity.validation_set.select_related().all():
                validation.delete()
            for extra_tab in activity.extra_tab_set.select_related().all():
                for param in extra_tab.parameter_set.select_related().all():
                    param.delete()
                extra_tab.delete()
            for action in activity.action_definition_set.select_related().all(
            ):
                for param in action.parameter_set.select_related().all():
                    param.delete()
                action.delete()
            activity.delete()

        for participant in ParticipantDefinition.objects.all():
            participant.delete()
        for application_parameter in ApplicationParameterDefinition.objects.all(
        ):
            application_parameter.delete()
        for application in ApplicationDefinition.objects.all():
            application.delete()
        for flow in FlowDefinition.objects.all():
            flow.delete()
        for package in FlowPackage.objects.all():
            package.delete()

    @classmethod
    def delete_subscriptions_by_flow_definition(cls, flow_definition):
        for subscription_event in flow_definition.source_event_set.select_related(
        ).all():
            for action in subscription_event.action_set.select_related().all():
                for parameter in action.parameter_set.select_related.all():
                    parameter.delete()
                action.delete()
            for subscription_object in subscription_event.source_object_set.select_related(
            ).all():
                subscription_object.delete()
            subscription_event.delete()

    @classmethod
    def delete_cases_by_flow_definition(cls, flow_definition):
        for flow_case in flow_definition.flow_case_set.select_related().all():
            flow_case.delete_flow_case()
