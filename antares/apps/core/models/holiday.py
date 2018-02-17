from datetime import datetime, timedelta
import logging
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

logger = logging.getLogger(__name__)


class Holiday(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))

    holiday_name = models.CharField(
        max_length=300,
        verbose_name=_(__name__ + ".holiday_name"),
        help_text=_(__name__ + ".holiday_name_help"))
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".description"),
        help_text=_(__name__ + ".description_help"))
    holiday_date = models.DateField(
        unique=True,
        verbose_name=_(__name__ + ".holiday_date"),
        help_text=_(__name__ + ".holiday_date_help"))
    recurrent_every_year = models.BooleanField(
        default=False,
        verbose_name=_(__name__ + ".recurrent_every_year"),
        help_text=_(__name__ + ".recurrent_every_year_help"))
    active = models.BooleanField(
        default=True,
        verbose_name=_(__name__ + ".active"),
        help_text=_(__name__ + ".active_help"))
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
        super(Holiday, self).save(*args, **kwargs)

    def __str__(self):
        if (self.name):
            return self.name
        return str(self.id)

    @classmethod
    def next_day(cls,
                 day,
                 consider_saturdays=True,
                 consider_sundays=True,
                 consider_holidays=True):
        """
        Gets the next available working day.
        """
        #so we only work with full days.
        if isinstance(day, datetime):
            day = day.date()
        day = day + timedelta(days=1)
        if ((consider_saturdays == True and day.isoweekday() == 6)
                or (consider_sundays == True and day.isoweekday() == 7)):
            return Holiday.next_day(day, consider_saturdays, consider_sundays,
                                    consider_holidays)
        elif consider_holidays == True:
            try:
                holiday = Holiday.objects.get(holiday_date=day, active=True)
                logger.info(
                    _(__name__ +
                      ".skiping_found_holiday_in_database %(holiday)d ") %
                    {'holiday': holiday})
                Holiday.next_day(day, consider_saturdays, consider_sundays,
                                 consider_holidays)
            except Holiday.DoesNotExist:
                return day
        else:
            return day

    @classmethod
    def prev_day(cls,
                 day,
                 consider_saturdays=True,
                 consider_sundays=True,
                 consider_holidays=True):
        """
        Gets the previous available working day.
        """

        if isinstance(day, datetime):
            day = day.date()
        day = day - timedelta(days=1)
        if ((consider_saturdays == True and day.isoweekday() == 6)
                or (consider_sundays == True and day.isoweekday() == 7)):
            return Holiday.prev_day(
                day - timedelta(days=1),
                consider_saturdays,
                consider_sundays,
                consider_holidays)
        elif consider_holidays == True:
            try:
                holiday = Holiday.objects.get(holiday_date=day, active=True)
                logger.info(
                    _(__name__ +
                      ".skiping_found_holiday_in_database %(holiday)d ") %
                    {'holiday': holiday})
                Holiday.prev_day(day, consider_saturdays, consider_sundays,
                                 consider_holidays)
            except Holiday.DoesNotExist:
                return day
        else:
            return day

    class Meta:
        app_label = 'core'
        db_table = 'core_holiday'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
