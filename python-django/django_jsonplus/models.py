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
