from django import template
from django.utils.translation import ugettext as _
from renderformplain.utils import render_field


register = template.Library()


@register.filter
def data(field, empty_value=_(u'-- undefined --')):
    return render_field(field, empty_value)