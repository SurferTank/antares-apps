from antares.apps.core.middleware.request import get_request
import logging

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
import js2py


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def extra_tabs_index(context):
    activity = context['activity']
    extra_tabs = ""
    for extra_tab in activity.activity_definition.extra_tab_set.select_related(
    ).all():
        extra_tabs += '<li><a data-toggle="tab" href="#{href}">{name}</a></li>'.format(
            href=extra_tab.tab_id, name=extra_tab.tab_name)

    return mark_safe(extra_tabs)


@register.simple_tag(takes_context=True)
def extra_tabs_content(context):
    activity = context['activity']
    extra_tabs = ""
    for extra_tab in activity.activity_definition.extra_tab_set.select_related(
    ).all():
        extra_tabs += '<div id="{tab_id}" class="tab-pane fade"><div id="{tab_id}_content"></div></div>'.format(
            tab_id=extra_tab.tab_id)
        if (extra_tab.route):
            extra_tabs += '<script>$("#{tab_id}_content").load("{url}?'.format(
                tab_id=extra_tab.tab_id, url=reverse(extra_tab.route))
            for param in extra_tab.parameter_set.select_related().all():
                param_value = _eval_extra_tab_value(activity, param.value)
                if (param_value):
                    extra_tabs += '&{param_id}={value}'.format(
                        param_id=param.param_id, value=param_value)
            extra_tabs += '&activity_id={activity_id}&is_inner=yes");</script>'.format(
                activity_id=activity.id)

        elif (extra_tab.url):
            extra_tabs += '<script>$("#{tab_id}_content").load("{url}?'.format(
                tab_id=extra_tab.tab_id, url=extra_tab.url)
            for param in extra_tab.parameter_set.select_related().all():
                param_value = _eval_extra_tab_value(activity, param.value)
                if (param_value):
                    extra_tabs += '&{param_id}={value}'.format(
                        param_id=param.param_id, value=param_value)
            extra_tabs += '&activity_id={activity_id}");</script>'.format(
                activity_id=activity.id)
    return mark_safe(extra_tabs)


@register.simple_tag(takes_context=True)
def doc_create_dropdown_menu(context):
    activity = context['activity']
    documents = ""
    for form in activity.activity_definition.form_set.select_related().filter(
            can_create=True).all():
        params_str = ""
        if (form.can_save == True):
            standard_params = '&activity_id={activity_id}&next={next}'.format(
                activity_id=activity.id,
                next=reverse(
                    'antares.apps.flow:dashboard_view',
                    kwargs={'activity_id': str(activity.id)}))
        else:
            standard_params = '&activity_id={activity_id}&next={next}&ss=true'.format(
                activity_id=activity.id,
                next=reverse(
                    'antares.apps.flow:dashboard_view',
                    kwargs={'activity_id': str(activity.id)}))
        for param in form.parameter_set.select_related().all():
            param_value = _eval_form_value(activity, param.value)
            if (param_value):
                params_str += '&{param_id}={value}'.format(
                    param_id=param.param_id, value=param_value)
        if (params_str):
            documents += '<li><a href="{doc_route}?{params_str}{standard_params}">{form_name}</a></li>'.format(
                doc_route=reverse(
                    'antares.apps.document:create_view',
                    kwargs={'form_id': form.form_definition.id}),
                params_str=params_str,
                standard_params=standard_params,
                form_name=form.form_definition.id)
    if documents:
        dropdown_menu = """<div class="dropdown">
  <button class="btn btn-default dropdown-toggle" type="button" id="documentCreateDropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    {label}
    <span class="caret"></span>
  </button>
  <ul class="dropdown-menu dropdown-menu-right aria-labelledby="documentCreateDropdownMenu">
    {documents}
  </ul>
    </div>""".format(
            label="Create Document", documents=documents)
        return mark_safe(dropdown_menu)
    else:
        return ""


def _eval_extra_tab_value(activity, value):
    if (value):
        context = js2py.EvalJs({
            'flow_case': activity.flow_case,
            'activity': activity,
            'logger': logger,
            'user': get_request().user
        })
        # here we return the values as it is
        try:
            context.execute('return_value = ' + value)
            if (hasattr(context, 'return_value')):
                return context.return_value
            else:
                return None
        except:
            return None
    else:
        return None


def _eval_form_value(activity, value):
    if (value):
        context = js2py.EvalJs({
            'flow_case': activity.flow_case,
            'activity': activity,
            'logger': logger,
            'user': get_request().user
        })
        # here we return the values as it is
        try:
            context.execute('return_value = ' + value)
            if (hasattr(context, 'return_value')):
                return context.return_value
            else:
                return None
        except:
            return None
    else:
        return None
