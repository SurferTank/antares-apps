import logging

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from enumfields import EnumField
from django.conf import settings


logger = logging.getLogger(__name__)


class SystemParameter(models.Model):
    id = models.SlugField(
        primary_key=True,
        max_length=255,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".description"),
        help_text=_(__name__ + ".description_help"))
    boolean_value = models.NullBooleanField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".boolean_value"),
        help_text=_(__name__ + ".boolean_value_help"))
    data_type = EnumField(
        FieldDataType,
        max_length=20,
        verbose_name=_(__name__ + ".data_type"),
        help_text=_(__name__ + ".data_type_help"))
    date_value = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".date_value"),
        help_text=_(__name__ + ".date_value_help"))
    float_value = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".float_value"),
        help_text=_(__name__ + ".float_value_help"))
    integer_value = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".integer_value"),
        help_text=_(__name__ + ".integer_value_help"))
    string_value = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".string_value"),
        help_text=_(__name__ + ".string_value_help"))
    text_value = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".text_value"),
        help_text=_(__name__ + ".text_value_help"))
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
        if get_request() is not None:
            self.author = get_request().user
            
        super(SystemParameter, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    @staticmethod
    def find_one(system_paramId,
                 paramType=None,
                 default=None,
                 description=None):
        try:
            system_param = SystemParameter.objects.get(id=system_paramId)
            logger.info("we have it! " + system_param.id)
            if system_param.data_type == FieldDataType.STRING:
                return system_param.string_value
            elif system_param.data_type == FieldDataType.TEXT:
                return system_param.text_value
            elif system_param.data_type == FieldDataType.DATE:
                return system_param.date_value
            elif system_param.data_type == FieldDataType.INTEGER:
                return system_param.integer_value
            elif system_param.data_type == FieldDataType.FLOAT:
                return system_param.decimal_value
            elif system_param.data_type == FieldDataType.UUID:
                return system_param.string_value
            elif system_param.data_type == FieldDataType.BOOLEAN:
                return system_param.boolean_value
            else:
                return None
        except SystemParameter.DoesNotExist:
            system_param = SystemParameter(id=system_paramId)
            logger.info("creating system parameter")
            if (description is not None):
                system_param.description = description

            if paramType == FieldDataType.STRING:
                system_param.string_value = default
                system_param.data_type = paramType
                system_param.save()
                return default
            elif paramType == FieldDataType.TEXT:
                system_param.text_value = default
                system_param.data_type = paramType
                system_param.save()
                return default
            elif paramType == FieldDataType.DATE:
                system_param.date_value = default
                system_param.data_type = paramType
                system_param.save()
                return default
            elif paramType == FieldDataType.INTEGER:
                system_param.integer_value = default
                system_param.data_type = paramType
                system_param.save()
                return default
            elif paramType == FieldDataType.FLOAT:
                system_param.float_value = default
                system_param.data_type = paramType
                system_param.save()
                return default
            elif paramType == FieldDataType.UUID:
                system_param.string_value = default
                system_param.data_type = paramType
                system_param.save()
                return default
            elif paramType == FieldDataType.BOOLEAN:
                system_param.boolean_value = default
                system_param.data_type = paramType
                system_param.save()
                return default
            else:
                return None

    class Meta:
        app_label = 'core'
        db_table = 'core_system_parameter'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
