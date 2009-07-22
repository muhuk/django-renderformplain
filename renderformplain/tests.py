from django.test import TestCase
from django import forms
from utils import get_field_display, get_field_data, get_choice


class FieldValueTestCase(TestCase):
    choices = (('X', u'xxx'),
               ('Y', u'yyy'),
               ('Z', u'zzz'))

    msg_field_data = 'get_field_data failed for %sform boolean field with ' \
                     '`%s` value.'
    msg_field_display = 'get_field_display failed for %sform boolean field' \
                        ' with `%s` value.'

    def _test_form(self):
        class TestForm(forms.Form):
            boolean_field = forms.BooleanField()
            char_field = forms.CharField()
            choice_field = forms.ChoiceField(choices=self.choices)
            date_field = forms.DateField()
            integer_field = forms.IntegerField()
        return TestForm

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
