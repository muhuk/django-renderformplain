from django.forms.forms import BoundField
from django.forms.widgets import Widget
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from utils import render_field


class PlainTextWidget(Widget):
    def __init__(self, form, field_name, attrs=None, tag_name=u'span'):
        super(PlainTextWidget, self).__init__(attrs)
        self.form = form
        self.field_name = field_name
        self.tag_name = tag_name

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        value = render_field(BoundField(self.form,
                                        self.form.fields[self.field_name],
                                        self.field_name))
        return mark_safe(u'<%s%s>%s</%s>' % (self.tag_name,
                                              flatatt(final_attrs),
                                              value,
                                              self.tag_name))
