from __future__ import absolute_import, print_function
from collections import namedtuple
from datetime import datetime

from django.test import TestCase
from django.db import connection

from moneyed import Money
from djmoney.money import Money as DjangoMoney
import jsonplus

from tests.models import TestModel


class SimpleTest(TestCase):
    def read(self, fieldname='normal'):
        with connection.cursor() as cursor:
            cursor.execute("SELECT %s FROM tests_testmodel" % fieldname)
            return cursor.fetchone()[0]

    def test_str(self):
        orig = TestModel.objects.create(normal="value")
        copy = TestModel.objects.get(id=orig.id)
        self.assertEqual(orig.normal, copy.normal)

    def test_none(self):
        orig = TestModel.objects.create(normal=1, nullable=None)
        copy = TestModel.objects.get(id=orig.id)
        self.assertEqual(orig.nullable, copy.nullable)

    def test_none_repr(self):
        orig = TestModel.objects.create(normal=1, nullable=None)
        indb = self.read('nullable')
        self.assertEqual(orig.nullable, indb)

    def test_dict(self):
        orig = TestModel.objects.create(normal={"x": [1,2,3]})
        copy = TestModel.objects.get(id=orig.id)
        self.assertEqual(orig.normal, copy.normal)

    def test_inf(self):
        orig = TestModel.objects.create(normal=float('inf'))
        copy = TestModel.objects.get(id=orig.id)
        self.assertEqual(orig.normal, copy.normal)

    def test_namedtuple(self):
        Point = namedtuple('Point', 'x y')
        orig = TestModel.objects.create(normal=Point(3, 4))
        copy = TestModel.objects.get(id=orig.id)
        self.assertNotEqual(id(orig.normal), id(copy.normal))
        self.assertEqual(copy.normal.x, 3)
        self.assertEqual(copy.normal.y, 4)
        self.assertEqual(orig.normal, copy.normal)

    def test_datetime(self):
        orig = TestModel.objects.create(normal=datetime.now())
        copy = TestModel.objects.get(id=orig.id)
        self.assertEqual(orig.normal, copy.normal)

    def test_django_money(self):
        m = Money(313, 'USD')
        dm = DjangoMoney(313, 'USD')
        obj = jsonplus.loads(jsonplus.dumps(dm))
        self.assertEqual(obj, dm)
        self.assertTrue(hasattr(obj, 'is_localized'))
        self.assertTrue(hasattr(dm, 'is_localized'))
        self.assertFalse(hasattr(m, 'is_localized'))