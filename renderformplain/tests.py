from django.test import TestCase
from django import forms
from django import template
from forms import PlainTextWidget
from utils import get_field_display, get_field_data, get_choice


class BaseTestCase(TestCase):
    choices = (('X', u'xxx'),
               ('Y', u'yyy'),
               ('Z', u'zzz'))

    def _test_form(self):
        class TestForm(forms.Form):
            boolean_field = forms.BooleanField()
            char_field = forms.CharField()
            choice_field = forms.ChoiceField(choices=self.choices)
            date_field = forms.DateField()
            integer_field = forms.IntegerField()
        return TestForm


class FieldValueTestCase(BaseTestCase):
    msg_field_data = 'get_field_data failed for %sform boolean field with ' \
                     '`%s` value.'
    msg_field_display = 'get_field_display failed for %sform boolean field' \
                        ' with `%s` value.'

    def test_boolean_field(self):
        for value in (True, False):
            for kwarg in ('initial', 'data'):
                form = self._test_form()(**{kwarg: {'boolean_field': value}})
                self.assertEqual(get_field_data(form['boolean_field']),
                                 value,
                                 self.msg_field_data % (
                                    form.is_bound and 'bound ' or '',
                                    str(value)))
                self.assertEqual(get_field_display(form['boolean_field']),
                                 value,
                                 self.msg_field_display % (
                                    form.is_bound and 'bound ' or '',
                                    str(value)))

    def test_char_field(self):
        value = u'\u011e\xdc\u015e\u0130\xd6\xc7' # GUSIOC with accents
        for kwarg in ('initial', 'data'):
            form = self._test_form()(**{kwarg: {'char_field': value}})
            self.assertEqual(get_field_data(form['char_field']),
                             value,
                             self.msg_field_data % (
                                form.is_bound and 'bound ' or '',
                                value.encode('utf8')))
            self.assertEqual(get_field_display(form['char_field']),
                             value,
                             self.msg_field_display % (
                                form.is_bound and 'bound ' or '',
                                value.encode('utf8')))

    def test_choice_field(self):
        msg_choice = 'get_choice failed for choice key `%s`.'
        self.assertEqual(get_choice(self.choices, None), None)
        self.assertEqual(get_choice(self.choices, u'Non-existent-key'),
                         u'Non-existent-key')
        for key, display in self.choices:
            for kwarg in ('initial', 'data'):
                form = self._test_form()(**{kwarg: {'choice_field': key}})
                self.assertEqual(get_choice(self.choices, key),
                                 display,
                                 msg_choice % key)
                self.assertEqual(get_field_data(form['choice_field']),
                                 key,
                                 self.msg_field_data % (
                                     form.is_bound and 'bound ' or '', key))
                self.assertEqual(get_field_display(form['choice_field']),
                                 display,
                                 self.msg_field_display % (
                                    form.is_bound and 'bound ' or '',
                                    display.encode('utf8')))

    def test_date_field(self):
        value = u'2000-01-01'
        for kwarg in ('initial', 'data'):
            form = self._test_form()(**{kwarg: {'date_field': value}})
            self.assertEqual(get_field_data(form['date_field']),
                             value,
                             self.msg_field_data % (
                                 form.is_bound and 'bound ' or '',
                                 value.encode('utf8')))
            self.assertEqual(get_field_display(form['date_field']),
                             value,
                             self.msg_field_display % (
                                 form.is_bound and 'bound ' or '',
                                 value.encode('utf8')))

    def test_integer_field(self):
        value = 123456
        for kwarg in ('initial', 'data'):
            form = self._test_form()(**{kwarg: {'integer_field': value}})
            self.assertEqual(get_field_data(form['integer_field']),
                             value,
                             self.msg_field_data % (
                                 form.is_bound and 'bound ' or '', str(value)))
            self.assertEqual(get_field_display(form['integer_field']),
                             value,
                             self.msg_field_display % (
                                 form.is_bound and 'bound ' or '', str(value)))


class PlainTextWidgetTestCase(BaseTestCase):
    def test_widget(self):
        value_dict = {'boolean_field': True,
                      'char_field': u'XYZ',
                      'choice_field': 'Z',
                      'integer_field': 42,
                      'date_field': '1980-05-20'}
        form = self._test_form()(value_dict)
        bound_fields = {}
        for field_name, field in form.fields.items():
            field.widget = PlainTextWidget(form, field_name)
            bound_fields[field_name] = forms.forms.BoundField(form,
                                                              field,
                                                              field_name)
        self.assertEqual(unicode(bound_fields['boolean_field']),
                         u'<span id="id_boolean_field"><input checked="' \
                         u'checked" readonly="True" type="checkbox"' \
                         u' name="boolean_field" /></span>')
        self.assertEqual(unicode(bound_fields['char_field']),
                         u'<span id="id_char_field">XYZ</span>')
        self.assertEqual(unicode(bound_fields['choice_field']),
                         u'<span id="id_choice_field">zzz</span>')
        self.assertEqual(unicode(bound_fields['integer_field']),
                         u'<span id="id_integer_field">42</span>')
        self.assertEqual(unicode(bound_fields['date_field']),
                         u'<span id="id_date_field">20.05.1980</span>')


class TagsAndFiltersTestCase(BaseTestCase):
    base_template = u'{%% load renderformplain_tags %%}\n\n%s\n'

    def _render_test_template(self, tmpl):
        value_dict = {'boolean_field': False,
                    'char_field': u'Abc',
                    'choice_field': 'Y',
                    'integer_field': 404,
                    'date_field': '2005-02-18'}

        tmpl = template.Template(tmpl)
        for kwarg in ('initial', 'data'):
            form = self._test_form()(**{kwarg: value_dict})
            context = template.Context({'form': form})
            result = tmpl.render(context)
            for value in (u'type="checkbox"',
                          u'Abc',
                          u'yyy',
                          u'404',
                          u'18.02.2005'):
                self.assert_(value in result)

    def test_data_filter(self):
        tmpl = self.base_template % u'{{ form.boolean_field|data }}' \
                                    u' {{ form.char_field|data }}' \
                                    u' {{ form.choice_field|data }}' \
                                    u' {{ form.integer_field|data }}' \
                                    u' {{ form.date_field|data }}'
        self._render_test_template(tmpl)

    def test_plainform_tag(self):
        tmpl = self.base_template % u'{% plainform form as plain_form %}' \
                                    u' {{ plain_form.as_p }}'
        self._render_test_template(tmpl)
