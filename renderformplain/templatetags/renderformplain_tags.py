from django import template
from django.forms import CheckboxInput
from django.utils.translation import ugettext as _
from django.utils.html import escape
from renderformplain.utils import get_field_display


register = template.Library()


@register.filter
def data(field, empty_value=_(u'-- undefined --')):
    value = get_field_display(field)
    if value is None or value == u'':
        return empty_value
    # We don't want to print True or False in case of a CheckBox widget
    elif isinstance(field.field.widget, CheckboxInput):
        return field.field.widget.render(field.name,
                                         value,
                                         attrs={'readonly': True})
    return escape(value)
