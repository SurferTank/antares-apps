'''
Created on 28 sep. 2016

@author: leobelen
'''
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def on_behalf_selector(context):
    request = context['request']
    try:
        command_string = """<form class="navbar-search pull-right"><select class="navbar-btn auth_on_behalf_selector">
        <option value="{id}" selected="selected">{text}</option>
    </select>
    </form>
    <style>
    select[class*="auth_on_behalf_selector"] {{
    margin-bottom: 0;
    }}
    </style>
    <script type="text/javascript">
$(document).ready(function() {{
  $(".auth_on_behalf_selector").select2({{
  'ajax': {{
    'url': "{url_selector}",
    'dataType': 'json',
    'delay': 250,
    'method': 'POST', 
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
$(".auth_on_behalf_selector").on("change", function (e) {{
     $.ajax({{
        'url': "{url_change}",
        'dataType': 'json',
        'method': 'POST', 
        'data': {{
             'csrfmiddlewaretoken': $.cookie('csrftoken'),
             'client_id': $(".auth_on_behalf_selector option:selected").val()
         }},
         'success': function(result){{
             location.reload();
         }}
     }});
     
}});
</script>""".format(
            url_selector=reverse('antares.apps.user:api_on_behalf_selector'),
            url_change=reverse(
                'antares.apps.user:api_on_behalf_change_client'),
            id=request.user.get_on_behalf_client().id,
            text=request.user.get_on_behalf_client().code + ' - ' + 
            request.user.get_on_behalf_client().full_name)
        return mark_safe(command_string)
    except:
        return ''


@register.simple_tag(takes_context=True)
def draw_site_nav(context):
    request = context['request']
    command = ""
    try:
        app_list = request.user.get_application_list()
        for app in app_list:
            command += process_site_nav(app)
    except:
        pass
    return mark_safe(command)


@register.simple_tag(takes_context=True)
def draw_site_menu(context):
    request = context['request']
    command = ""
    try:
        app_list = request.user.get_application_list()
        if (len(app_list) > 0):
            command += '<div class="row">'
        for app in app_list:
            command += process_site_menu_app(app)

        if (len(app_list) > 0):
            command += '</div>'
    except:
        pass
    return mark_safe(command)


def process_site_menu_app(app):
    command = '<div class="menu_level_{app_level}">'.format(
        app_level=app.level)
    if app.url:
        command += '<a href="{url}">{name}</a>'.format(
            url=app.url, name=app.name)
    elif app.route:
        command += '<a href="{route}">{name}</a>'.format(
            route=reverse(app.route), name=app.name)
    command += '</div>'
    return command


def process_site_nav(app):
    command = '<li>'
    if app.url:
        command += '<a href="{url}">{name}</a>'.format(
            url=app.url, name=app.name)
    elif app.route:
        command += '<a href="{route}">{name}</a>'.format(
            route=reverse(app.route), name=app.name)
    command += '</li>'
    return command
