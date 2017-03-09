from django.db import models
from django_jsonplus.models import JSONPlusField


class TestModel(models.Model):
    normal = JSONPlusField()
    nullable = JSONPlusField(null=True, blank=True)
