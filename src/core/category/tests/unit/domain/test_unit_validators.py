import unittest

from core.category.domain.validators import CategoryValidator, CategoryValidatorFactory


class TestCategoryValidatorUnit(unittest.TestCase):
    validator: CategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory.create()
        return super().setUp()

    def test_invalidation_cases_for_name_field(self):
        invalid_data = [
            {'data': None, 'expected': 'This field is required.'},
            {'data': {}, 'expected': 'This field is required.'},
            {'data': {'name': ''}, 'expected': 'This field may not be blank.'},
            {'data': {'name': None}, 'expected': 'This field may not be null.'},
            {'data': {'name': 5}, 'expected': 'Not a valid string.'},
            {'data': {'name': 'a' * 256},
                'expected': 'Ensure this field has no more than 255 characters.'},
        ]
        for data in invalid_data:
            is_valid = self.validator.validate(data['data'])
            self.assertFalse(is_valid)
            self.assertListEqual(
                self.validator.errors['name'], [data['expected']],
                f'Expected: {data["expected"]}, actual: {self.validator.errors["name"][0]}')

    def test_invalidation_cases_for_description_field(self):
        is_valid = self.validator.validate({'description': 5})
        self.assertFalse(is_valid)
        self.assertListEqual(self.validator.errors['description'], [
                             'Not a valid string.'])

    def test_invalidation_cases_for_is_active_field(self):
        expected_data = [
            {'data': None, 'expected': 'This field may not be null.'},
            {'data': 0, 'expected': 'Must be a valid boolean.'},
            {'data': 'True', 'expected': 'Must be a valid boolean.'},
        ]

        for data in expected_data:
            is_valid = self.validator.validate({'is_active': data['data']})
            self.assertFalse(is_valid)
            self.assertListEqual(
                self.validator.errors['is_active'], [data['expected']])

    def test_invalidation_cases_for_created_at_field(self):
        expected_data = [
            {'data': None, 'expected': 'This field may not be null.'},
            {'data': 5, 'expected': 'Datetime has wrong format. Use one of these formats instead: '
                                    'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'},
        ]

        for data in expected_data:
            is_valid = self.validator.validate({'created_at': data['data']})
            self.assertFalse(is_valid)
            self.assertListEqual(
                self.validator.errors['created_at'], [data['expected']])

    def test_valid_cases(self):
        valid_data = [
            {'data': {'name': 'name'}},
            {'data': {'name': 'name', 'description': 'description'}},
            {'data': {'name': 'name', 'description': 'description', 'is_active': True}},
            {'data': {'name': 'name', 'description': 'description', 'is_active': False}},
        ]

        for data in valid_data:
            is_valid = self.validator.validate(data['data'])
            self.assertTrue(is_valid)
            # print(self.validator.validated_data)
            self.assertDictEqual(data['data'], self.validator.validated_data)
