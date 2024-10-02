from django.utils import timezone
import unittest

import pytest
from core.category.infra.django_app.models import CategoryModel


@pytest.mark.django_db()
class TestCategoryModelInt(unittest.TestCase):

    def test_foo(self):
        arrange = {
            'id' : 'f6e70586-a265-439e-9424-340adda215f9',
            'name' : 'movie',
            'description' : None,
            'is_active' : True,
            'created_at' : timezone.now()
        }
        
        category = CategoryModel.objects.create(**arrange)
        self.assertEqual(category.id, arrange['id'])
        self.assertEqual(category.name, arrange['name'])
        self.assertEqual(category.description, arrange['description'])
        self.assertEqual(category.is_active, arrange['is_active'])
        self.assertEqual(category.created_at, arrange['created_at'])
