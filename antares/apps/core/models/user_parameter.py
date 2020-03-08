import datetime
import logging
from uuid import UUID

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request

from .system_parameter import SystemParameter


logger = logging.getLogger(__name__)


class UserParameter(models.Model):
    id = models.SlugField(
        primary_key=True,
        max_length=255,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".user"),
        help_text=_(__name__ + ".user_help"),
        blank=True,
        null=True)
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".description"),
        help_text=_(__name__ + ".description_help"))
    data_type = models.TextField(
        choices=FieldDataType.choices,
        max_length=20,
        verbose_name=_(__name__ + ".data_type"),
        help_text=_(__name__ + ".data_type_help"))
    boolean_value = models.NullBooleanField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".boolean_value"),
        help_text=_(__name__ + ".boolean_value_help"))
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

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        super(UserParameter, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    @classmethod
    def find_one(cls,
                 user_paramId,
                 paramType=None,
                 default=None,
                 fall_down_on_user_params=True):
        """
        Retrieves a parameter from the user parameter database
        """
        try:
            user_param = cls.objects.get(
                id=user_paramId, user=get_request().user)
            if user_param.data_type == FieldDataType.STRING:
                return user_param.string_value
            elif user_param.data_type == FieldDataType.TEXT:
                return user_param.text_value
            elif user_param.data_type == FieldDataType.DATE:
                if isinstance(user_param.date_value, datetime.datetime):
                    return user_param.date_value.date()
                if isinstance(user_param.date_value, datetime.date):
                    return user_param.date_value
            elif user_param.data_type == FieldDataType.DATETIME:
                if isinstance(user_param.date_value, datetime.datetime):
                    return user_param.date_value
                elif isinstance(user_param.date_value, datetime.date):
                    return datetime.datetime.combine(
                        user_param.date_value, datetime.datetime.min.time())

            elif user_param.data_type == FieldDataType.INTEGER:
                return user_param.integer_value
            elif user_param.data_type == FieldDataType.FLOAT:
                return float(user_param.float_value)
            elif user_param.data_type == FieldDataType.UUID:
                try:
                    return UUID(user_param.string_value)
                except:
                    return None
            elif user_param.data_type == FieldDataType.BOOLEAN:
                return user_param.boolean_value
            else:
                return None
        except cls.DoesNotExist:
            if (fall_down_on_user_params == True and default is not None):
                user_parameter = SystemParameter.find_one(
                    user_paramId, paramType, default)
                return cls.find_one(user_paramId, paramType, user_parameter,
                                    False)
            if (default is not None):
                user_param = UserParameter(id=user_paramId)
                logger.debug("Creating the parameter with id " + str(user_paramId) +
                             " since it does not exist")
                user_param.data_type = paramType
                user_param.user = get_request().user
                if paramType == FieldDataType.STRING:
                    user_param.string_value = default
                    user_param.save()
                    return default
                elif paramType == FieldDataType.TEXT:
                    user_param.text_value = default
                    user_param.save()
                    return default
                elif paramType == FieldDataType.DATE:
                    user_param.date_value = default
                    user_param.save()
                    return default
                elif paramType == FieldDataType.DATETIME:
                    user_param.date_value = default
                    user_param.save()
                    return default
                elif paramType == FieldDataType.INTEGER:
                    user_param.integer_value = default
                    user_param.save()
                    return default
                elif paramType == FieldDataType.FLOAT:
                    user_param.float_value = default
                    user_param.save()
                    return default
                elif paramType == FieldDataType.UUID:
                    user_param.string_value = str(default)
                    user_param.save()
                    return default
                elif paramType == FieldDataType.BOOLEAN:
                    user_param.boolean_value = default
                    user_param.save()
                    return default
                else:
                    return None
            else:
                return None

    class Meta:
        app_label = 'core'
        db_table = 'core_user_parameter'
        unique_together = (('id', 'user'), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
