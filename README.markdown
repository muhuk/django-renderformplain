**django-renderformplain** provides template tags that allow you to render form fields in plaintext.


Features
========

::TODO


Installation
============

 1. Add `django-renderformplain` directory to your Python path.
 2. Add `renderformplain` to your `INSTALLED_APPS` tuple
    found in your settings file.


Testing & Example
=================

::TODO


Usage
=====

 1. Load renderformplain tags in your template with
    `{% load renderformplain_tags %}`.
 2. You can create a plaintext rendering copy of a form with
    `{% plainform some_form as new_variable %}` and then render normally;
    `{{ new_variable|as_p }}`.
 3. You can output just one field's data with
    `{{ some_form.field_name|data }}`.
 4. You can use `PlainTextWidget` in your own forms.
