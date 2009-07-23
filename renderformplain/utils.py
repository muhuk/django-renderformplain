import datetime
from django.forms.forms import BoundField
from django.forms import ValidationError, CheckboxInput
from django.forms import BooleanField, DateField, DateTimeField, TimeField
from django.template.defaultfilters import date, time
from django.utils.translation import ugettext as _
from django.utils.html import escape
from django.utils.safestring import mark_safe


def get_field_display(field):
    """
    Return the field value or the choice value (if choices are present) for a
    given form field.
    """
    if isinstance(field, BoundField):
        data = get_field_data(field)
        if hasattr(field.field, 'choices'):
            return get_choice(field.field.choices, data)
        else:
            return data
    raise ValueError('field must be a BoundField instance. Got %s instead' % \
                                                                  type(field))


def get_field_data(field):
    """
    Return field data for given field.

    Return initial data if the form is not bound.
    """
    if field.form.is_bound:
        return field.data
    else:
        data = field.form.initial.get(field.name, field.field.initial)
        if callable(data):
            data = data()
        return data


def get_choice(choices, key):
    """
    Return choice value if given choice key is in choices. Otherwise return
    `None`.
    """
    if key is None:
        return None
    # Cast key into choice key type if needed. We get might keys as string for
    # non-string fields. First choice key might be None
    choice_key_type = choices[0][0] is not None and type(choices[0][0]) \
                                                        or type(choices[1][0])
    if choice_key_type != type(key):
        key = choice_key_type(key)
    # Find the value of the choice or (worst-case) return key
    for choice in choices:
        if choice[0] == key:
            return choice[1]
    return key


def render_field(field, empty_value=_(u'-- undefined --'), value=None):
    value = value or get_field_display(field)
    if value is None or value == u'':
        return empty_value
    # Try to validate value to get internal Python types.
    # We need this to check if we can apply special formatting.
    if not hasattr(field.field, 'choices'):
        try:
            value = field.field.clean(value)
        except ValidationError:
            pass
    # We don't want to print True or False in case of a CheckBox widget.
    if isinstance(field.field, BooleanField):
        return CheckboxInput(field.field.widget.attrs).render(field.name,
                                              value, attrs={'readonly': True})
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

