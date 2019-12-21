import logging

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
import js2py

from antares.apps.accounting.models import AccountBalance
from antares.apps.accounting.models import AccountTransaction
from antares.apps.core.middleware.request import get_request
from django.conf import settings

from antares.apps.core.enums import HrnModuleType, ScriptEngineType, FieldDataType
from antares.apps.core.models.system_parameter import SystemParameter

logger = logging.getLogger(__name__)


class HrnCode(models.Model):
    """
    This class produces unique numbers and IDs to identify objects in a human readable manner, to avoid showing the
    confusing UUIDs...
    """
    id = models.SlugField(
        primary_key=True,
        max_length=50,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    organizational_unit = models.ForeignKey(
        'user.OrgUnit',
        on_delete=models.PROTECT,
        db_column='organizational_unit',
        verbose_name=_(__name__ + ".organizational_unit"),
        help_text=_(__name__ + ".organizational_unit_help"),
        blank=True,
        null=True)
    form_definition = models.ForeignKey(
        'document.FormDefinition',
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".form_definition"),
        help_text=_(__name__ + ".form_definition_help"),
        db_column='form_definition',
        blank=True,
        null=True)
    flow_definition = models.ForeignKey(
        'flow.FlowDefinition',
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".flow_definition"),
        help_text=_(__name__ + ".flow_definition_help"),
        db_column='flow_definition',
        blank=True,
        null=True)
    hrn_name = models.CharField(
        max_length=100,
        verbose_name=_(__name__ + ".hrn_name"),
        help_text=_(__name__ + ".hrn_name_help"),
        blank=True,
        null=True)
    description = RichTextField(
        verbose_name=_(__name__ + ".description"),
        help_text=_(__name__ + ".description_help"),
        blank=True,
        null=True)
    module_type  = models.CharField(
        max_length=20,
        choices=HrnModuleType.choices,
        default=HrnModuleType.DOCUMENT,
        verbose_name=_(__name__ + ".module_type"),
        help_text=_(__name__ + ".module_type_help")
    )
    number_code = models.BigIntegerField(
        verbose_name=_(__name__ + ".number_code"),
        help_text=_(__name__ + ".number_code_help"),
        blank=True,
        null=True)
    period = models.IntegerField(
        verbose_name=_(__name__ + ".period"),
        help_text=_(__name__ + ".period_help"),
        blank=True,
        null=True)
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".creation_name"),
        help_text=_(__name__ + ".creation_name_help"))
    update_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".update_date"),
        help_text=_(__name__ + ".update_date_help"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".author"),
        help_text=_(__name__ + ".author_help"))

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(HrnCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    @classmethod
    def find_one(cls, hrn_id):
        """
        Finds one Human Readable Code (HRN) or return None
        """
        try:
            return HrnCode.objects.get(pk=hrn_id)
        except HrnCode.DoesNotExist:
            return None

    @classmethod
    def _get_next_hrn_by_params(cls, module, hrn_id, **kwargs):
        """
            Gets the next HRN Code based on parameters
            
        """
        if module is None or hrn_id is None:
            raise ValueError(
                _('antares.apps.core.hrn_code.missing_key_elements'))
        if isinstance(module, str):
            module = HrnModuleType.to_enum(module)

        if kwargs.get('form_definition'):
            from antares.apps.document.models import FormDefinition
            form_definition = FormDefinition.find_one(
                kwargs.get('form_definition'))
            if form_definition is None:
                raise ValueError(
                    _(__name__ + ".exceptions.form_definition_was_not_found"))
        else:
            form_definition = None
        if kwargs.get('period'):
            period = int(float(kwargs.get('period')))
        else:
            period = None
        if kwargs.get('org_unit'):
            raise NotImplementedError
        else:
            org_unit = None

        if (form_definition is None and period is None and org_unit is None):
            # standard case
            hrn = HrnCode.find_one(hrn_id)
            if hrn is None:
                hrn = HrnCode()
                hrn.id = hrn_id
                hrn.module_type = module
                hrn.number_code = 1
                hrn.save()
                return hrn.number_code
            else:
                hrn.number_code = hrn.number_code + 1
                hrn.save()
                return hrn.number_code
        else:
            # other cases not implemented.
            raise NotImplementedError

    @classmethod
    def process_document_hrn_script(cls, document, event_type):
        """ 
        Gets a new HRN Code based on the document definition 
        """
        hrn_node = document.document_xml.find(
            'headerElements/options/hrnScript')
        if hrn_node is None or not hrn_node.text:
            document.set_header_field(
                'hrn_code',
                HrnCode._get_next_hrn_by_params(HrnModuleType.DOCUMENT,
                                                "GENERAL_DOCUMENT_SEQUENCE"))
            return

        language = ScriptEngineType.to_enum(hrn_node.get('language'))
        execution_string = hrn_node.text
        document = document
        header_fields = document.get_header_field_dict(False)
        if language is None:
            language = ScriptEngineType.to_enum(
                SystemParameter.find_one('DEFAULT_SCRIPT_ENGINE',
                                         FieldDataType.STRING,
                                         ScriptEngineType.JAVASCRIPT))
        if execution_string is None:
            document.set_header_field(
                'hrn_code',
                HrnCode._get_next_hrn_by_params("Document",
                                                "GENERAL_DOCUMENT_SEQUENCE"))
            return document

        if language == ScriptEngineType.PYTHON:
            # remember to return a dictionary with two values, hrn_string and
            # hrn_tile
            value = eval(execution_string)
            if value.get('hrn_code'):
                document.set_header_field("hrn_code", value.get('hrn_code'))
            else:
                # default value
                document.set_header_field(
                    'hrn_code',
                    HrnCode._get_next_hrn_by_params(
                        HrnModuleType.DOCUMENT, "GENERAL_DOCUMENT_SEQUENCE"))
            if value.get('hrn_title'):
                document.set_header_field("hrn_title", value.get('hrn_title'))
        elif ScriptEngineType.JAVASCRIPT:
            context = js2py.EvalJs({
                'event_type': event_type.value,
                'fields': document.get_field_dict(),
                'header_fields': header_fields,
                'document': document,
                'logger': logger,
                'HrnCode': HrnCode,
                'user': get_request().user
            })
            # here we return the values as it is, jst hrn_script and hrn_title
            context.execute(execution_string)
            if (hasattr(context, 'hrn_code') and context.hrn_code is not None):
                document.set_header_field("hrn_code", context.hrn_code)
            else:
                # default value
                document.set_header_field(
                    'hrn_code',
                    HrnCode._get_next_hrn_by_params(
                        HrnModuleType.DOCUMENT, "GENERAL_DOCUMENT_SEQUENCE"))

            if (hasattr(context, 'hrn_title')
                    and context.hrn_title is not None):
                document.set_header_field("hrn_title", context.hrn_title)
        return document

    @classmethod
    def process_flow_case_hrn_script(cls, flow_case):
        """ 
        Gets a new HRN Code based on the flow definition 
        """
        hrn_script = flow_case.flow_definition.hrn_script
        if not hrn_script:
            flow_case.hrn_code = HrnCode._get_next_hrn_by_params(
                HrnModuleType.FLOW_CASE, "GENERAL_FLOW_CASE_SEQUENCE")
            return flow_case

        language = ScriptEngineType.to_enum(
            SystemParameter.find_one('DEFAULT_SCRIPT_ENGINE',
                                     FieldDataType.STRING,
                                     ScriptEngineType.JAVASCRIPT))

        if language == ScriptEngineType.PYTHON:
            # remember to return a dictionary with two values, hrn_string and
            # hrn_tile
            value = eval(hrn_script)
            if value.get('hrn_code'):
                flow_case.hrn_code = value.get('hrn_code')
            else:
                flow_case.hrn_script = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.FLOW_CASE, "GENERAL_FLOW_CASE_SEQUENCE")

        elif ScriptEngineType.JAVASCRIPT:
            context = js2py.EvalJs({
                'flow_case': flow_case,
                'logger': logger,
                'HrnCode': HrnCode,
                'user': get_request().user
            })
            context.execute(hrn_script)
            if (hasattr(context, 'hrn_code') and context.hrn_code is not None):
                flow_case.hrn_code = context.hrn_code
            else:
                flow_case.hrn_code = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.FLOW_CASE, "GENERAL_FLOW_CASE_SEQUENCE")
                return flow_case
        return flow_case

    @classmethod
    def process_flow_activity_hrn_script(cls, flow_activity):
        """ 
        Gets a new HRN Code based on the activity 
        """
        hrn_script = flow_activity.flow_case.flow_definition.hrn_script
        if not hrn_script:
            flow_activity.hrn_code = HrnCode._get_next_hrn_by_params(
                HrnModuleType.FLOW_ACTIVITY, "GENERAL_FLOW_ACTIVITY_SEQUENCE")
            return flow_activity

        language = ScriptEngineType.to_enum(
            SystemParameter.find_one('DEFAULT_SCRIPT_ENGINE',
                                     FieldDataType.STRING,
                                     ScriptEngineType.JAVASCRIPT))

        if language == ScriptEngineType.PYTHON:
            # remember to return a dictionary with two values, hrn_string and
            # hrn_tile
            value = eval(hrn_script)
            if value.get('hrn_code'):
                flow_activity.hrn_code = value.get('hrn_code')
            else:
                flow_activity.hrn_code = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.FLOW_ACTIVITY,
                    "GENERAL_FLOW_ACTIVITY_SEQUENCE")
                return flow_activity

        elif ScriptEngineType.JAVASCRIPT:
            context = js2py.EvalJs({
                'activity': flow_activity,
                'logger': logger,
                'HrnCode': HrnCode,
                'user': get_request().user
            })
            context.execute(hrn_script)
            if (hasattr(context, 'hrn_code') and context.hrn_code is not None):
                flow_activity.hrn_code = context.hrn_code
            else:
                flow_activity.hrn_code = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.FLOW_ACTIVITY,
                    "GENERAL_FLOW_ACTIVITY_SEQUENCE")
                return flow_activity
        return flow_activity

    @classmethod
    def process_account_balance_hrn_script(
            cls, account_balance: AccountBalance) -> AccountBalance:
        """ 
        Gets a new HRN Code based on the account type 
        """
        hrn_script = account_balance.account_type.hrn_script
        if not hrn_script:
            account_balance.hrn_code = HrnCode._get_next_hrn_by_params(
                HrnModuleType.ACCOUNT_BALANCE,
                "GENERAL_ACCOUNT_BALANCE_SEQUENCE")
            return account_balance

        language = ScriptEngineType.to_enum(
            SystemParameter.find_one('DEFAULT_SCRIPT_ENGINE',
                                     FieldDataType.STRING,
                                     ScriptEngineType.JAVASCRIPT))

        if language == ScriptEngineType.PYTHON:
            # remember to return a dictionary with two values, hrn_string and
            # hrn_tile
            value = eval(hrn_script)
            if value.get('hrn_code'):
                account_balance.hrn_code = value.get('hrn_code')
            else:
                account_balance.hrn_script = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.ACCOUNT_BALANCE,
                    "GENERAL_ACCOUNT_BALANCE_SEQUENCE")

        elif ScriptEngineType.JAVASCRIPT:
            context = js2py.EvalJs({
                'account_balance': account_balance,
                'logger': logger,
                'HrnCode': HrnCode,
                'user': get_request().user
            })
            context.execute(hrn_script)
            if (hasattr(context, 'hrn_code') and context.hrn_code is not None):
                account_balance.hrn_code = context.hrn_code
            else:
                account_balance.hrn_script = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.ACCOUNT_BALANCE,
                    "GENERAL_ACCOUNT_BALANCE_SEQUENCE")
                return account_balance
        return account_balance

    @classmethod
    def process_account_transaction_hrn_script(
            cls,
            account_transaction: AccountTransaction) -> AccountTransaction:
        """ 
        Gets a new HRN Code based on the transaction type
        """
        hrn_script = account_transaction.transaction_type_type.hrn_script
        if not hrn_script:
            account_transaction.hrn_code = HrnCode._get_next_hrn_by_params(
                HrnModuleType.ACCOUNT_TRANSACTION,
                "GENERAL_ACCOUNT_TRANSACTION_SEQUENCE")
            return account_transaction

        language = ScriptEngineType.to_enum(
            SystemParameter.find_one('DEFAULT_SCRIPT_ENGINE',
                                     FieldDataType.STRING,
                                     ScriptEngineType.JAVASCRIPT))

        if language == ScriptEngineType.PYTHON:
            # remember to return a dictionary with two values, hrn_string and
            # hrn_tile
            value = eval(hrn_script)
            if value.get('hrn_code'):
                account_transaction.hrn_code = value.get('hrn_code')
            else:
                account_transaction.hrn_script = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.ACCOUNT_TRANSACTION,
                    "GENERAL_ACCOUNT_TRANSACTION_SEQUENCE")

        elif ScriptEngineType.JAVASCRIPT:
            context = js2py.EvalJs({
                'transaction': account_transaction,
                'logger': logger,
                'HrnCode': HrnCode,
                'user': get_request().user
            })
            context.execute(hrn_script)
            if (hasattr(context, 'hrn_code') and context.hrn_code is not None):
                account_transaction.hrn_code = context.hrn_code
            else:
                account_transaction.hrn_script = HrnCode._get_next_hrn_by_params(
                    HrnModuleType.ACCOUNT_TRANSACTION,
                    "GENERAL_ACCOUNT_TRANSACTION_SEQUENCE")
                return account_transaction
        return account_transaction

    class Meta:
        app_label = 'core'
        db_table = 'core_hrn_code'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
