import logging

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from enumfields import EnumField
from django.conf import settings

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
    data_type = EnumField(
        FieldDataType,
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
                 user,
                 userParamId,
                 paramType=None,
                 default=None,
                 fall_down_on_system_params=True):
        """
        Retrieves a parameter from the user parameter database
        """
        try:
            userParam = cls.objects.get(id=userParamId, user=user)
            logger.info("we have it! " + userParam.id)
            if userParam.data_type == FieldDataType.STRING:
                return userParam.string_value
            elif userParam.data_type == FieldDataType.TEXT:
                return userParam.text_value
            elif userParam.data_type == FieldDataType.DATE:
                return userParam.date_value
            elif userParam.data_type == FieldDataType.INTEGER:
                return userParam.integer_value
            elif userParam.data_type == FieldDataType.FLOAT:
                return userParam.decimal_value
            elif userParam.data_type == FieldDataType.UUID:
                return userParam.string_value
            elif userParam.data_type == FieldDataType.BOOLEAN:
                return userParam.boolean_value
            else:
                return None
        except cls.DoesNotExist:
            if (fall_down_on_system_params == True and default is not None):
                system_parameter = SystemParameter.find_one(
                    userParamId, paramType, default)
                return UserParameter.find_one(get_request().user, userParamId,
                                              paramType, system_parameter,
                                              False)
            if (default is not None):
                userParam = UserParameter(id=userParamId)
                logger.info("creating userParam")
                if paramType == FieldDataType.STRING:
                    userParam.string_value = default
                    userParam.user = user
                    userParam.data_type = paramType
                    userParam.save()
                    return default
                elif paramType == FieldDataType.TEXT:
                    userParam.text_value = default
                    userParam.user = user
                    userParam.data_type = paramType
                    userParam.save()
                    return default
                elif paramType == FieldDataType.DATE:
                    userParam.date_value = default
                    userParam.user = user
                    userParam.data_type = paramType
                    userParam.save()
                    return default
                elif paramType == FieldDataType.INTEGER:
                    userParam.string_value = default
                    userParam.user = user
                    userParam.data_type = paramType
                    userParam.save()
                    return default
                elif paramType == FieldDataType.FLOAT:
                    userParam.float_value = default
                    userParam.user = user
                    userParam.data_type = paramType
                    userParam.save()
                    return default
                elif paramType == FieldDataType.UUID:
                    userParam.string_value = default
                    userParam.user = user
                    userParam.data_type = paramType
                    userParam.save()
                    return default
                elif paramType == FieldDataType.BOOLEAN:
                    userParam.boolean_value = default
                    userParam.user = user
                    userParam.data_type = paramType
                    userParam.save()
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
