from django import template
from django.utils.translation import ugettext as _
from renderformplain.utils import render_field
from renderformplain.forms import convert_to_plainform


register = template.Library()


@register.filter
def data(field, empty_value=_(u'-- undefined --')):
    return render_field(field, empty_value)


class PlainformNode(template.Node):
    def __init__(self, form_var, plain_form_var):
        self.form_var = template.Variable(form_var)
        self.plain_form_var = plain_form_var

    def render(self, context):
        form = self.form_var.resolve(context)
        plain_form = convert_to_plainform(form)
        context[self.plain_form_var] = plain_form
        return ''


@register.tag
def plainform(parser, token):
    bits = token.split_contents()
    if len(bits) != 4 or bits[2] != u'as':
        raise template.TemplateSyntaxError
    return PlainformNode(bits[1], bits[3])