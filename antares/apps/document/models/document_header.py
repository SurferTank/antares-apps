import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from ..constants import DocumentAssociationType, DocumentOriginType, DocumentStatusType


logger = logging.getLogger(__name__)


class DocumentHeader(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    form_definition = models.ForeignKey(
        "FormDefinition",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".form_definition"),
        help_text=_(__name__ + ".form_definition_help"),
        db_column='form_definition',
        blank=True,
        null=True)
    delete_case = models.ForeignKey(
        "flow.FlowCase",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".delete_case"),
        help_text=_(__name__ + ".delete_case_help"),
        db_column='delete_case',
        blank=True,
        null=True,
        related_name="document_header_delete_case_set")
    related_case = models.ForeignKey(
        "flow.FlowCase",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".related_case"),
        help_text=_(__name__ + ".related_case_help"),
        db_column='related_case',
        blank=True,
        null=True,
        related_name="document_header_related_case_set")
    secondary_client = models.ForeignKey(
        "client.Client",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".secondary_client"),
        help_text=_(__name__ + ".secondary_client_help"),
        db_column='secondary_client',
        blank=True,
        null=True,
        related_name="document_header_secondary_client_set")
    user_referral = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".user_referral"),
        help_text=_(__name__ + ".user_referral_help"),
        db_column='user_referral',
        blank=True,
        null=True)
    cancel_case = models.ForeignKey(
        "flow.FlowCase",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".cancel_case"),
        help_text=_(__name__ + ".cancel_case_help"),
        db_column='cancel_case',
        blank=True,
        null=True,
        related_name="document_header_cancel_case_set")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".author"),
        help_text=_(__name__ + ".author_help"),
        db_column='author',
        blank=True,
        null=True,
        related_name="document_header_author_set")
    concept_type = models.ForeignKey(
        "core.ConceptType",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".concept_type"),
        help_text=_(__name__ + ".concept_type_help"),
        db_column='concept_type',
        blank=True,
        null=True)
    client = models.ForeignKey(
        "client.Client",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".client"),
        help_text=_(__name__ + ".client_help"),
        db_column='client',
        blank=True,
        null=True,
        related_name="document_header_client_set")
    branch = models.ForeignKey(
        "client.ClientBranch",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".branch"),
        help_text=_(__name__ + ".branch_help"),
        db_column='branch',
        blank=True,
        null=True,
        related_name="document_header_branch_set")
    account_document = models.ForeignKey(
        "accounting.AccountDocument",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".account_document"),
        help_text=_(__name__ + ".account_document_help"),
        db_column='account_document',
        blank=True,
        null=True)
    account_type = models.ForeignKey(
        "accounting.AccountType",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".account_type"),
        help_text=_(__name__ + ".account_type_help"),
        db_column='account_type',
        blank=True,
        null=True)
    associated_case = models.ForeignKey(
        "flow.FlowCase",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".associated_case"),
        help_text=_(__name__ + ".associated_case_help"),
        db_column='associated_case',
        blank=True,
        null=True,
        related_name="document_header_associated_case_set")
    base_document = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".base_document"),
        help_text=_(__name__ + ".base_document_help"),
        db_column='base_document',
        blank=True,
        null=True)
    period = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".period"),
        help_text=_(__name__ + ".period_help"))
    active_version = models.BooleanField(
        default=True,
        verbose_name=_(__name__ + ".active_version"),
        help_text=_(__name__ + ".active_version_help"))
    associated_to = models.ForeignKey(
        "DocumentHeader",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".associated_to"),
        help_text=_(__name__ + ".associated_to_help"),
        related_name='associated_document_header_set',
        blank=True,
        null=True)
    association_type = models.CharField(choices=DocumentAssociationType.choices,
        max_length=30,
        default=DocumentAssociationType.NONE,
        verbose_name=_(__name__ + ".association_type"),
        help_text=_(__name__ + ".association_type_help"))
    cancel_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".cancel_date"),
        help_text=_(__name__ + ".cancel_date_help"))
    creation_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_(__name__ + ".creation_date"),
        help_text=_(__name__ + ".creation_date_help"))
    delete_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".delete_date"),
        help_text=_(__name__ + ".delete_date_help"))
    document_number = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".document_number"),
        help_text=_(__name__ + ".document_number_help"))
    document_version = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".document_version"),
        help_text=_(__name__ + ".document_version_help"))
    draft_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".draft_date"),
        help_text=_(__name__ + ".draft_date_help"))
    hash = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".hash"),
        help_text=_(__name__ + ".hash_help"))
    hrn_code = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_(__name__ + ".hrn_code"),
        help_text=_(__name__ + ".hrn_code_help"))
    hrn_title = models.CharField(
        max_length=4000,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".hrn_title"),
        help_text=_(__name__ + ".hrn_title_help"))
    origin = models.CharField(choices=DocumentOriginType.choices,
        max_length=30,
        default=DocumentOriginType.UNKNOWN,
        verbose_name=_(__name__ + ".origin"),
        help_text=_(__name__ + ".origin_help"))
    save_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".save_date"),
        help_text=_(__name__ + ".save_date_help"))
    status = models.CharField(choices=DocumentStatusType.choices,
        max_length=30,
        default=DocumentStatusType.DRAFTED,
        verbose_name=_(__name__ + ".status"),
        help_text=_(__name__ + ".status_help"))
    default_currency = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".default_currency"),
        help_text=_(__name__ + ".default_currency_help"))

    @classmethod
    def find_one(cls, document_id):
        try:
            return cls.objects.get(pk=document_id)
        except DocumentHeader.DoesNotExist:
            return None

    @classmethod
    def find_one_by_hrn_code(cls, hrn_code):
        try:
            return cls.objects.get(hrn_code=hrn_code)
        except DocumentHeader.DoesNotExist:
            return None

    class Meta:
        app_label = 'document'
        db_table = 'doc_header'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
