import unittest
from __seedwork.domain.exceptions import ValidationException
from category.domain.entities import Category


class TestCategoryIntegration(unittest.TestCase):
    def test_create_with_invalid_cases_for_name_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None)
        self.assertEqual(assert_error.exception.args[0], 'name is required')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name='')
        self.assertEqual(assert_error.exception.args[0], 'name is required')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name=5)
        self.assertEqual(
            assert_error.exception.args[0], 'name must be a string')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name='a' * 256)
        self.assertEqual(
            assert_error.exception.args[0], 'name must be at most 255 characters long')

    def test_create_with_invalid_cases_for_description_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name='Movie', description=5)
        self.assertEqual(
            assert_error.exception.args[0], 'description must be a string')

    def test_create_with_invalid_cases_for_is_active_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name='Movie', is_active='True')
        self.assertEqual(
            assert_error.exception.args[0], 'is_active must be a boolean')

    def test_create_with_valid_cases(self):
        try:
            Category(name='Movie')
            Category(name='Movie', description='A description')
            Category(name='Movie', description='A description', is_active=True)
        except ValidationException as exception:
            self.fail(f'Some prop is not valid. Error: {exception.args[0]}')

    def test_update_with_invalid_cases_for_name_prop(self):
        category = Category(name='Movie')
        with self.assertRaises(ValidationException) as assert_error:
            category.update(None, None)
        self.assertEqual(assert_error.exception.args[0], 'name is required')

        with self.assertRaises(ValidationException) as assert_error:
            category.update('', None)
        self.assertEqual(assert_error.exception.args[0], 'name is required')

        with self.assertRaises(ValidationException) as assert_error:
            category.update(5, None)
        self.assertEqual(
            assert_error.exception.args[0], 'name must be a string')

        with self.assertRaises(ValidationException) as assert_error:
            category.update('a' * 256, None)
        self.assertEqual(
            assert_error.exception.args[0], 'name must be at most 255 characters long')

    def test_update_with_invalid_cases_for_description_prop(self):
        category = Category(name='Movie')
        with self.assertRaises(ValidationException) as assert_error:
            category.update('Movie', 5)
        self.assertEqual(
            assert_error.exception.args[0], 'description must be a string')

    def test_update_with_valid_cases(self):
        category = Category(name='Movie')
        try:
            category.update('Movie 2', None)
            category.update('Movie 3', 'A description')
        except ValidationException as exception:
            self.fail(f'Some prop is not valid. Error: {exception.args[0]}')
