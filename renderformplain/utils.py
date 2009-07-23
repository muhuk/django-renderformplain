from django.forms.forms import BoundField


def get_field_display(field):
    """
    Return the field value or the choice value (if choices are present) for a
    given form field.
    """
    if isinstance(field, BoundField):
        data = get_field_data(field)
        if hasattr(field.field.widget, 'choices'):
            return get_choice(field.field.widget.choices, data)
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
