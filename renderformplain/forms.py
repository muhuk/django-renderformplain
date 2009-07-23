from django.forms.widgets import Widget
from django.forms.util import flatatt
from django.utils.safestring import mark_safe


class PlainTextWidget(Widget):
    def __init__(self, attrs=None, tag_name=u'span'):
        super(PlainTextWidget, self).__init__(attrs)
        self.tag_name = tag_name

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        return mark_safe(u'<%s%s>%s</%s>' % (self.tag_name,
                                              flatatt(final_attrs),
                                              value,
                                              self.tag_name))
