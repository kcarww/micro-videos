import pytest
import unittest
from django.utils import timezone
from core.category.domain.entities import Category
from core.category.infra.django_app.models import CategoryModel
from django.db import models

@pytest.mark.django_db()
class TestCategoryModelInt(unittest.TestCase):

    def test_mapping(self):
        table_name = CategoryModel._meta.db_table
        self.assertEqual(table_name, 'categories')
        
        fields_name = tuple(field.name for field in CategoryModel._meta.fields)
        self.assertEqual(fields_name, ('id', 'name', 'description', 'is_active', 'created_at'))
        
        id_field: models.UUIDField = CategoryModel.id.field
        self.assertIsInstance(id_field, models.UUIDField)
        self.assertTrue(id_field.primary_key)
        self.assertIsNone(id_field.db_column)
        self.assertTrue(id_field.editable)
        
        name_field: models.CharField = CategoryModel.name.field
        self.assertIsInstance(name_field, models.CharField)
        self.assertIsNone(name_field.db_column)
        self.assertFalse(name_field.null)
        self.assertFalse(name_field.blank)
        self.assertEqual(name_field.max_length, 255)
        
        
        created_at_field: models.DateTimeField = CategoryModel.created_at.field
        self.assertIsInstance(created_at_field, models.DateTimeField)
        self.assertIsNone(created_at_field.db_column)
        self.assertFalse(created_at_field.null)

    
    # def test_foo(self):
    #     arrange = {
    #         'id' : 'f6e70586-a265-439e-9424-340adda215f9',
    #         'name' : 'movie',
    #         'description' : None,
    #         'is_active' : True,
    #         'created_at' : timezone.now()
    #     }
        
    #     category = CategoryModel.objects.create(**arrange)
    #     self.assertEqual(category.id, arrange['id'])
    #     self.assertEqual(category.name, arrange['name'])
    #     self.assertEqual(category.description, arrange['description'])
    #     self.assertEqual(category.is_active, arrange['is_active'])
    #     self.assertEqual(category.created_at, arrange['created_at'])
