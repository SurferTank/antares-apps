'''
Created on Jul 25, 2016

@author: leobelen
'''
from antares.apps.core.middleware.request import get_request
import logging
import urllib
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
import js2py
from mptt.models import MPTTModel, TreeForeignKey

from ..constants import ApplicationScopeType


logger = logging.getLogger(__name__)


class Application(MPTTModel):
    """

    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    application_name = models.CharField(max_length=200)
    url = models.CharField(max_length=300, blank=True, null=True)
    route = models.CharField(max_length=300, blank=True, null=True)
    scope = models.CharField(choices=ApplicationScopeType.choices,
                             max_length=30, default=ApplicationScopeType.SELF)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_application_author_set",
        editable=False)

    def get_parameter_name_list(self):
        result = []
        for param in self.parameter_set.select_related().all():
            result.append(param.parameter_name)
        return result

    def get_parameter_value_list(self):
        result = []
        for param in self.parameter_set.select_related().all():
            result.append(param.value)
        return result

    def get_first_parameter_value(self):
        params = self.parameter_set.select_related().all()
        if len(params) > 0:
            return params[0].value
        return None

    def get_parameter_string(self, only_routes=False):
        result = ""
        first_one = True
        for param in self.parameter_set.select_related().all():
            if (param.is_route_parameter == True and only_routes == True):
                if (param.is_named_route_parameter == True):
                    result += " " + param.parameter_name + "=\"" + str(
                        self._evaluate_param(param.value)) + "\""
                else:
                    result += " \"" + str(self._evaluate_param(
                        param.value)) + "\""
            elif (param.is_route_parameter == False and only_routes == False):
                if first_one == True:
                    first_one = False
                    result = "?"
                else:
                    result += "&"
                    result += param.parameter_name + "=" + str(
                        self._evaluate_param(param.value))
        if result == "":
            return
        else:
            return result

    def get_route_parameter_string(self):
        return self.get_parameter_string(True)

    def get_url_parameter_string(self):
        return self.get_parameter_string(False)

    def _evaluate_param(self, parameter_code):
        context = js2py.EvalJs({'user': get_request().user})
        context.execute('result = ' + parameter_code)
        if (hasattr(context, 'result') and context.result is not None):
            return context.result
        else:
            return ""

    def as_url_string(self):
        url = ""
        parameters = self.parameter_set.select_related()
        if self.url:
            url += self.url
        elif self.route:
            params = {}
            if parameters.filter(is_route_parameter=True).count() > 0:
                for param in parameters.filter(is_route_parameter=True).all():
                    params[param.parameter_name] = str(
                        self._evaluate_param(param.value))
                url += reverse(self.route, kwargs=params)
            else:
                url += reverse(self.route)

        if parameters.filter(is_route_parameter=False).count() > 0:
            params = {}
            for param in parameters.filter(is_route_parameter=True).all():
                params[param.parameter_name] = str(
                    self._evaluate_param(param.value))
            uri_params = urllib.parse.urlencode(params)
            url += "/?" + uri_params
        return url

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(Application, self).save(*args, **kwargs)

    def __str__(self):
        if self.application_name is None:
            return str(self.id)
        else:
            return self.application_name

    class Meta:
        app_label = 'user'
        db_table = 'user_application'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")

    class MPTTMeta:
        order_insertion_by = ['id']
