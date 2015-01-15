from django import template
from django.template import Context
from django.contrib.auth.models import User
from django.template import RequestContext

register = template.Library()

@register.inclusion_tag('sm_00/navigation.html', takes_context=True)
def show_nav(context):
    pass
#    print(context['request'].user)


@register.inclusion_tag('sm_00/guest_navigation.html')
def guest_show_nav():
    pass


@register.assignment_tag
def get_navigation_buttons():
    buttons = []
    buttons.append({'url':'/area', 'value':'Region'})
    buttons.append({'url':'/task', 'value':'Task'})
    buttons.append({'url':'/slave', 'value':'Slave'})
    buttons.append({'url':'/accounts/logout', 'value':'Logout'})
    return buttons


@register.assignment_tag
def guest_get_navigation_buttons():
    buttons = []
    buttons.append({'url':'/area', 'value':'Region'})
    buttons.append({'url':'/task', 'value':'Task'})
    buttons.append({'url':'/slave', 'value':'Slave'})
    buttons.append({'url':'/accounts/login', 'value':'Login'})

    return buttons

