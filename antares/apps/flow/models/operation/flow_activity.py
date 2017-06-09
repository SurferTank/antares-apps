import logging
import uuid

from django.core.urlresolvers import resolve
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import F
from django.db.models import Avg
from antares.apps.core.utils import DateUtils

from enumfields import EnumField
from django.conf import settings
from antares.apps.core.constants import FieldDataType

from antares.apps.flow.constants import FlowActivityStatusType, FlowDataType

logger = logging.getLogger(__name__)


class FlowActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='performer',
        related_name='flow_activity_set',
        blank=True,
        null=True)
    participant_definition = models.ForeignKey(
        "ParticipantDefinition",
        on_delete=models.PROTECT,
        related_name='activity_set',
        db_column='participant_definition',
        blank=True,
        null=True)
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        related_name='activity_set',
        db_column='flow_case')
    activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        related_name='activity_set',
        db_column='activity_definition')
    activity_number = models.CharField(max_length=255, blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField()
    start_date = models.DateTimeField(blank=True, null=True)
    status = EnumField(FlowActivityStatusType, max_length=30)
    status_date = models.DateTimeField()
    hrn_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_(__name__ + ".hrn_code"),
        help_text=_(__name__ + ".hrn_code_help"))

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.status_date = timezone.now()
        super(FlowActivity, self).save(*args, **kwargs)

    def __str__(self):
        if self.activity_number:
            return self.activity_number
        else:
            return str(self.id)
    
    def waiting_time(self):
        if (self.creation_date is not None 
            and self.start_date is not None
            and self.status not in 
            (FlowActivityStatusType.CREATED.value, FlowActivityStatusType.CANCELLED.value)):
            return DateUtils.convert_days_to_time_unit(self.start_date - self.creation_date, 
                                                       self.flow_case.flow_definition.duration)
        else:
            return None
    
    def working_time(self):
        if (self.start_date is not None 
            and self.completion_date is not None
            and self.status not in 
            (FlowActivityStatusType.CREATED.value, FlowActivityStatusType.CANCELLED.value, 
             FlowActivityStatusType.ACTIVE.value)):
            return DateUtils.convert_days_to_time_unit(self.completion_date - self.start_date, 
                                                       self.flow_case.flow_definition.duration)
        else:
            return None
    
    def duration(self):
        if (self.creation_date is not None 
            and self.completion_date is not None
            and self.status not in 
            (FlowActivityStatusType.CREATED.value, FlowActivityStatusType.CANCELLED.value, 
             FlowActivityStatusType.ACTIVE.value)):
            return DateUtils.convert_days_to_time_unit(self.completion_date - self.creation_date,
                                                       self.flow_case.flow_definition.duration)
        else:
            return None
    
    @classmethod 
    def find_average_waiting_time(cls, activity_def, perfomer=None):
        query = cls.objects.filter(activity_definition=activity_def).\
                filter(creation_date__is_null=False).\
                filter(start_date__is_null=False).\
                filter(status__not_in=[FlowActivityStatusType.CREATED.value, FlowActivityStatusType.CANCELLED.value])
                
        if perfomer is not None:
            query = query.filter(perfomer=perfomer)
        
        query = query.aggregate(average_difference=Avg(F('start_date') - F('creation_date')))
            
        return DateUtils.convert_days_to_time_unit(query, 
                activity_def.flow_case.flow_definition.duration)
    
    @classmethod 
    def find_average_working_time(cls, activity_def, perfomer=None):
        query = cls.objects.filter(activity_definition=activity_def).\
            filter(completion__is_null=False).\
            filter(start_date__is_null=False).\
            filter(status__not_in=[FlowActivityStatusType.CREATED.value, FlowActivityStatusType.CANCELLED.value, 
             FlowActivityStatusType.ACTIVE.value])
        
        if perfomer is not None:
            query = query.filter(perfomer=perfomer)
            
        query = query.aggregate(average_difference=Avg(F('completion_date') - F('start_date')))
        
        return  DateUtils.convert_days_to_time_unit(query,
                activity_def.flow_case.flow_definition.duration)
            
            
    
    @classmethod 
    def find_average_duration(cls, activity_def, perfomer=None):
        query = cls.objects.filter(activity_definition=activity_def).\
            filter(completion__is_null=False).\
            filter(creation_date__is_null=False).\
            filter(status__not_in=[FlowActivityStatusType.CREATED.value, FlowActivityStatusType.CANCELLED.value])
        
        if perfomer is not None:
            query = query.filter(perfomer=perfomer)
        query = query.aggregate(average_difference=Avg(F('completion_date') - F('creation_date')))
        
        return  DateUtils.convert_days_to_time_unit(query, activity_def.flow_case.flow_definition.duration)
    
    @classmethod
    def find_one(cls, doc_id):
        try:
            return FlowActivity.objects.get(id=doc_id)
        except FlowActivity.DoesNotExist:
            return None

    @classmethod
    def find_one_by_hrn_code(cls, hrn_code):
        try:
            return FlowActivity.objects.get(hrn_code=hrn_code)
        except FlowActivity.DoesNotExist:
            return None

    @classmethod
    def find_by_flow_case(cls, flow_case):
        try:
            return FlowActivity.objects.filter(flow_case=flow_case)
        except FlowActivity.DoesNotExist:
            return []

    @classmethod
    def find_by_flow_case_and_status(cls, flow_case, status):
        try:
            return FlowActivity.objects.filter(
                flow_case=flow_case, status=status)
        except FlowActivity.DoesNotExist:
            return []

    @classmethod
    def delete_by_flow_case(cls, flow_case):
        for activity in flow_case.activity_set.select_related().all():
            for activity_log in activity.select_related().all():
                activity_log.delete()
            activity.delete()

    @classmethod
    def find_unfinished_activities_by_flow_case_and_performer(
            cls, flow_case, performer):
        try:
            return flow_case.activity_set.select_related().filter(
                Q(status=FlowActivityStatusType.ACTIVE) |
                Q(status=FlowActivityStatusType.CREATED) |
                Q(status=FlowActivityStatusType.REASSIGNED),
                performer=performer)
        except FlowActivity.DoesNotExist:
            return []

    @classmethod
    def cancel_activity(cls, activity):
        activity.status = FlowActivityStatusType.CANCELLED
        activity.status_date = timezone.now()
        activity.save()
        return activity

    @classmethod
    def find_by_perfomer_and_status(cls, performer, status):
        try:
            return FlowActivity.objects.filter(
                performer=performer, status=status)
        except FlowActivity.DoesNotExist:
            return []

    def process_tools(self):
        """ 
        Processes an activity and outputs a list of commands ready to be posted in the page to further use. 
        """
        tools = []
        for app_definition in self.activity_definition.activity_application_definition_set.select_related(
        ):
            command = ""
            if app_definition.application_definition.application_id != 'updateproperty':
                if app_definition.application_definition.url:
                    command = "<a href=\"{url}\">{description}</a>".format(
                        url=app_definition.application_definition.url,
                        description=app_definition.application_definition.
                        description)
                else:
                    command = "<a href=\"{url}\">{description}</a>".format(
                        url=resolve(
                            app_definition.application_definition.route),
                        description=app_definition.application_definition.
                        description)

            else:
                if app_definition.description:
                    command = "<div>{description}</div>".format(
                        description=app_definition.description)
                else:
                    command = "<div>{description}</div>".format(
                        description=app_definition.application_definition.
                        application_id)

                for param in app_definition.parameter_definition_set.select_related(
                ).all():
                    for flow_property in self.flow_case.property_set.select_related(
                    ).all():
                        logger.info(
                            "prop id: {prop_id} param id: {param_id}".format(
                                prop_id=flow_property.property_id,
                                param_id=param.content))

                        if flow_property.property_id == param.content:
                            if flow_property.property_definition.data_type == FlowDataType.BASIC:
                                if flow_property.property_definition.sub_data_type == FieldDataType.BOOLEAN:
                                    form_string = "<form><input type=\"checkbox\" name=\"{parameter_id}_{definition_id}\" id=\"{parameter_id}_{definition_id}\" data-toggle=\"toggle\" " +\
                                    "{checked_value}/><div style=\"text-align: right;\"><a class=\"btn btn-default\" onclick=\"leftToolbarUpdateProperty(event, '{flow_case_id}'," +\
                                            " '{parameter_id}', $('#{parameter_id}_{definition_id}').prop('checked'));\" class=\"button round small\">" +\
                                            "{button_label}</a></div></form>"
                                    if flow_property.boolean_value == True:
                                        command += form_string.format(
                                            parameter_id=param.content,
                                            definition_id=app_definition.id,
                                            flow_case_id=self.flow_case.id,
                                            checked_value='checked',
                                            button_label=_(
                                                __name__ + ".buttons.save"))
                                    else:
                                        command += form_string.format(
                                            parameter_id=param.content,
                                            definition_id=app_definition.id,
                                            flow_case_id=self.flow_case.id,
                                            checked_value='',
                                            button_label=_(
                                                __name__ + ".buttons.save"))
                                else:
                                    if flow_property.property_definition.catalog:
                                        form_string = """<form><select name="{parameter_id}_{definition_id}" id="{parameter_id}_{definition_id}"><option value=''>--- {default_option_name} ---</option></select>
                                            <div style="text-align: right;"><a class="btn btn-default" onclick="leftToolbarUpdateProperty(event, '{flow_case_id}','{parameter_id}', $('#{parameter_id}_{definition_id}').val());" class="button round small">{button_label}</a></div>
                                            </form><script type="text/javascript">
                                                $(document).ready(function() {{
                                                      $("#{parameter_id}_{definition_id}").select2({{
                                                      'ajax': {{
                                                        'url': "{url}",
                                                        'dataType': 'json',
                                                        'delay': 250,
                                                        'method': 'GET', 
                                                        'data': function (params) {{
                                                          return {{
                                                            'q': params.term, // search term
                                                            'csrfmiddlewaretoken': $.cookie('csrftoken')
                                                          }};
                                                        }},
                                                        'processResults': function (data, params) {{
                                                             return {{
                                                                    results: data
                                                            }};
                                                        }},
                                                        'cache': true
                                                      }},
                                                      'minimumInputLength': 0,
                                                      }});
                                                    }});
                                                </script>"""

                                        url = "/antares/core/api/select_options" + '?selector=' + flow_property.property_definition.catalog
                                        command += form_string.format(
                                            parameter_id=param.content,
                                            definition_id=app_definition.id,
                                            flow_case_id=self.flow_case.id,
                                            url=url,
                                            default_option_name=_(
                                                __name__ +
                                                ".selector.default_option_text"
                                            ),
                                            button_label=_(
                                                __name__ + ".buttons.save"))
                                    else:
                                        form_string =  "<form><input type=\"text\" name=\"{parameter_id}_{definition_id}\" id=\"{parameter_id}_{definition_id}\"/>" +\
                                            "<div style=\"text-align: right;\"><a class=\"btn btn-default\" onclick=\"leftToolbarUpdateProperty(event, '{flow_case_id}',"+\
                                            " '{parameter_id}', $('#{parameter_id}_{definition_id}').val());\" class=\"button round small\">" +\
                                            "{button_label}</a></div></form>"
                                        command += form_string.format(
                                            parameter_id=param.content,
                                            definition_id=app_definition.id,
                                            flow_case_id=self.flow_case.id,
                                            button_label=_(
                                                __name__ + ".buttons.save"))

            tools.append(command)

        return tools

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
