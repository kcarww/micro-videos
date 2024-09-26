import unittest
from datetime import datetime
from dataclasses import FrozenInstanceError, is_dataclass
from unittest.mock import patch
from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        with patch.object(Category, 'validate') as mock_validate_method:
            data = datetime.now()
            category = Category(
                name='Movies', description='description', is_active=True, created_at=data)
            mock_validate_method.assert_called_once()
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
        with patch.object(Category, 'validate') as mock_validate_method:
            category1 = Category(name='Movies')
            mock_validate_method.assert_called_once()
            import time
            time.sleep(1)
            category2 = Category(name='Movies')
            self.assertNotEqual(category1.created_at.timestamp(),
                                category2.created_at.timestamp())

    def test_is_immutable(self):
        with patch.object(Category, 'validate'):
            with self.assertRaises(FrozenInstanceError):
                value_object = Category(name='teste')
                value_object.name = 'category'

    def test_activate(self):
        with patch.object(Category, 'validate'):
            category = Category(name='Movies', is_active=False)
            category.activate()
            self.assertTrue(category.is_active)

    def test_deactivate(self):
        with patch.object(Category, 'validate'):
            category = Category(name='Movies')
            category.deactivate()
            self.assertFalse(category.is_active)

    def test_update(self):
        with patch.object(Category, 'validate'):
            category = Category(name='Movies')
            category.update(name='Games', description='description')
            self.assertEqual(category.name, 'Games')
            self.assertEqual(category.description, 'description')
