import unittest
from category.domain.entities import Category
from datetime import datetime
from dataclasses import FrozenInstanceError, is_dataclass

class TestCategoryUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))
    
    def test_constructor(self):
        data = datetime.now()
        category = Category(name='Movies', description='description', is_active=True, created_at=data)
        self.assertEqual(category.name, 'Movies')
        self.assertEqual(category.description, 'description')
        self.assertEqual(category.is_active, True)
        self.assertEqual(category.created_at, data)
        
        category = Category(name='Movies')
        self.assertEqual(category.name, 'Movies')
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, datetime)
        
    def test_if_created_at_is_generated_in_constructor(self):
        category1 = Category(name='Movies')
        category2 = Category(name='Movies')
        self.assertNotEqual(category1.created_at.timestamp(),
                            category2.created_at.timestamp())
        
    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = Category(name='teste')
            value_object.name = 'category'
            
    
