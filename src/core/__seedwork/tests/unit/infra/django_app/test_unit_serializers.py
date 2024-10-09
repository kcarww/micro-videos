from typing import OrderedDict
import unittest

from core.__seedwork.application.dto import PaginationOutput
from core.__seedwork.infra.django_app.serializers import CollectionSerializer, PaginationSerializer
from rest_framework import serializers

class TestPaginationSerializer(unittest.TestCase):

    def test_serialize(self):
        pagination = {
            'current_page': '1',
            'per_page': '2',
            'last_page': '3',
            'total': '4'
        }
        data = PaginationSerializer(instance=pagination).data

        self.assertEqual(data, {
            'current_page': 1,
            'per_page': 2,
            'last_page': 3,
            'total': 4
        })


class StubSerializer(serializers.Serializer):
    name = serializers.CharField()


class StubCollectionSerializer(CollectionSerializer):
    child = StubSerializer()


class TestCollectionSerializer(unittest.TestCase):

    def test_if_throw_an_error_when_instance_is_not_a_pagination_output(self):
        error_message = 'Instance must be a PaginationOutput'
        with self.assertRaises(TypeError) as assert_exception:
            CollectionSerializer()
        self.assertEqual(str(assert_exception.exception), error_message)

        with self.assertRaises(TypeError):
            CollectionSerializer(instance={})
        self.assertEqual(str(assert_exception.exception), error_message)

        with self.assertRaises(TypeError):
            CollectionSerializer(instance=1)
        self.assertEqual(str(assert_exception.exception), error_message)

    def test__init__(self):
        pagination = PaginationOutput(
            items=[1, 2, 3],
            current_page=1,
            per_page=2,
            last_page=3,
            total=4
        )
        collection = StubCollectionSerializer(instance=pagination)
        self.assertEqual(collection.pagination, pagination)
        self.assertEqual(collection.instance, pagination.items)

    def test_serialize(self):
        pagination = PaginationOutput(
            items=[{'name': 'foo'}, {'name': 'bar'}],
            current_page='1',
            per_page='2',
            last_page='3',
            total='4'
        )
        data = StubCollectionSerializer(instance=pagination).data
        self.assertEqual(data, {
            'data': [
                OrderedDict([('name', 'foo')]),
                OrderedDict([('name', 'bar')])
            ],
            'meta': {
                'current_page': 1,
                'per_page': 2,
                'last_page': 3,
                'total': 4
            }
        })
