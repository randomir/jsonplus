Django-JSONPlus
===============

Django extension for non-basic types' serialization to JSON via jsonplus_ lib.

.. _jsonplus: https://pypi.python.org/pypi/jsonplus/


Install
-------

Install from PyPI::

    pip install django-jsonplus

Add to your ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        <other-apps>

        'django_jsonplus',
    ]


Usage
-----

To use ``jsonplus`` for database values (de-)serialization, use the
``JSONPlusField``:

.. code-block:: python

    from django.db import models
    from django.contrib.postgres.fields import JSONField
    from django_jsonplus.models import JSONPlusField

    class MyModel(models.Model):
        # stores only numbers, strings, lists, dicts (but not dates)
        basic_data = JSONField()

        # stores datetime, namedtuple, set, decimal, complex...
        rich_data = JSONPlusField()
