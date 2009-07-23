import datetime
from django import template
from django.template.defaultfilters import date, time
from django.forms import ValidationError
from django.forms import CheckboxInput, DateField, DateTimeField, TimeField
from django.utils.translation import ugettext as _
from django.utils.html import escape
from django.utils.safestring import mark_safe
from renderformplain.utils import get_field_display


register = template.Library()


@register.filter
def data(field, empty_value=_(u'-- undefined --')):
    value = get_field_display(field)
    # Try to validate value to get internal Python types.
    # We need this to check if we can apply special formatting.
    if not hasattr(field.field, 'choices'):
        try:
            value = field.field.clean(value)
        except ValidationError:
            pass
    if value is None or value == u'':
        return empty_value
    # We don't want to print True or False in case of a CheckBox widget.
    elif isinstance(field.field.widget, CheckboxInput):
        return field.field.widget.render(field.name,
                                         value,
                                         attrs={'readonly': True})
    # Format dates and times nicely.
    elif isinstance(field.field, DateField) and isinstance(value,
                                                               datetime.date):
        return date(value)
    elif isinstance(field.field, DateTimeField) and isinstance(value,
                                                           datetime.datetime):
        return mark_safe(u'%s %s' % (date(value), time(value)))
    elif isinstance(field.field, TimeField) and isinstance(value,
                                                               datetime.time):
        return time(value)
    return escape(value)
