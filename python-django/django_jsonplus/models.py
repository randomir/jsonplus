import six
import jsonplus

from django.db import models


class JSONPlusField(models.TextField):
    """Use jsonplus serializer to support custom python types, like
    `datetime`."""

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return jsonplus.loads(value)

    def to_python(self, value):
        if not isinstance(value, six.string_types):
            return value
        return jsonplus.loads(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return jsonplus.dumps(value)


# additional Django-specific encoders

from djmoney.money import Money as DjangoMoney

# TODO: add to jsonplus a way to hook encoder/decoder with a priority
# TODO: add to jsonplus unregister function
# NOTE: the line below is an abomination; used for test/prototype only
del jsonplus._encode_handlers['exact']['classname']['Money']

@jsonplus.encoder('DjangoMoney', lambda obj: isinstance(obj, DjangoMoney))
def _django_money_dumps(obj):
    return jsonplus.getattrs(obj, attrs=['amount', 'currency'])

@jsonplus.decoder('DjangoMoney')
def _django_money_loads(val):
    return DjangoMoney(**val)
