from dataclasses import fields
import unittest
from unittest.mock import MagicMock, PropertyMock, patch
from rest_framework.serializers import Serializer
from __seedwork.domain.exceptions import ValidationException
from __seedwork.domain.validators import DRFValidator, ValidatorFieldsInterface, ValidatorRules


class TestValidatorRulesUnit(unittest.TestCase):
    def test_values_method(self):
        validator = ValidatorRules.values('value1', 'prop1')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, 'value1')
        self.assertEqual(validator.prop, 'prop1')

    def test_required_rule(self):
        invalid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': '', 'prop': 'prop'},
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException,
                                   msg=f'value: {i["value"]}, prop: {i["prop"]}'
                                   ) as assert_erro:
                self.assertIsInstance(ValidatorRules.values(
                    i['value'], i['prop']).required(), ValidatorRules)

            self.assertEqual('prop is required', assert_erro.exception.args[0])

        valid_data = [
            {'value': 'value', 'prop': 'prop'},
            {'value': 0, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'},
        ]

        for i in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                i['value'], i['prop']).required(), ValidatorRules)

    def test_string_rule(self):
        invalid_data = [
            {'value': 0, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'},
            {'value': {}, 'prop': 'prop'}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException,
                                   msg=f'value: {i["value"]}, prop: {i["prop"]}'
                                   ) as assert_erro:
                self.assertIsInstance(ValidatorRules.values(
                    i['value'], i['prop']).string(), ValidatorRules)

            self.assertEqual('prop must be a string',
                             assert_erro.exception.args[0])

        valid_data = [
            {'value': 'value', 'prop': 'prop'},
            {'value': None, 'prop': 'prop'},
            {'value': "", 'prop': 'prop'},
        ]

        for i in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                i['value'], i['prop']).string(), ValidatorRules)

    def test_max_length_rule(self):
        invalid_data = [
            {'value': 'value', 'prop': 'prop', 'length': 4},
            {'value': 'value', 'prop': 'prop', 'length': 3},
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException,
                                   msg=f'value: {i["value"]}, prop: {i["prop"]}'
                                   ) as assert_erro:
                self.assertIsInstance(ValidatorRules.values(
                    i['value'], i['prop']).max_length(i['length']), ValidatorRules)

            self.assertEqual(f'prop must be at most {i["length"]} characters long',
                             assert_erro.exception.args[0])

        valid_data = [
            {'value': 'value', 'prop': 'prop', 'length': 5},
            {'value': 'value', 'prop': 'prop', 'length': 6},
            {'value': None, 'prop': 'prop', 'length': 4},
            {'value': "", 'prop': 'prop', 'length': 4},
        ]

        for i in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                i['value'], i['prop']).max_length(i['length']), ValidatorRules)

    def test_boolean(self):
        invalid_data = [
            {'value': 'value', 'prop': 'prop'},
            {'value': 0, 'prop': 'prop'},
            {'value': {}, 'prop': 'prop'}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException,
                                   msg=f'value: {i["value"]}, prop: {i["prop"]}'
                                   ) as assert_erro:
                self.assertIsInstance(ValidatorRules.values(
                    i['value'], i['prop']).boolean(), ValidatorRules)

            self.assertEqual('prop must be a boolean',
                             assert_erro.exception.args[0])

        valid_data = [
            {'value': True, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'},
            {'value': None, 'prop': 'prop'},
        ]

        for i in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                i['value'], i['prop']).boolean(), ValidatorRules)

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        with self.assertRaises(ValidationException) as assert_erro:
            ValidatorRules.values(
                None, 'prop').required().string().max_length(5)
        self.assertEqual('prop is required', assert_erro.exception.args[0])

        with self.assertRaises(ValidationException) as assert_erro:
            ValidatorRules.values(5, 'prop').required().string().max_length(5)

        self.assertEqual('prop must be a string',
                         assert_erro.exception.args[0])

        with self.assertRaises(ValidationException) as assert_erro:
            ValidatorRules.values(
                'valuee', 'prop').required().string().max_length(5)

        self.assertEqual('prop must be at most 5 characters long',
                         assert_erro.exception.args[0])

        with self.assertRaises(ValidationException) as assert_erro:
            ValidatorRules.values(
                None, 'prop').required().boolean()
        self.assertEqual('prop is required', assert_erro.exception.args[0])

        with self.assertRaises(ValidationException) as assert_erro:
            ValidatorRules.values('1', 'prop').required().boolean()

        self.assertEqual('prop must be a boolean',
                         assert_erro.exception.args[0])

    def test_valid_cases_for_combination_between_two_rules(self):
        ValidatorRules.values('value', 'prop').required().string()
        ValidatorRules.values(
            'value', 'prop').required().string().max_length(5)
        ValidatorRules.values(True, 'prop').required().boolean()
        ValidatorRules.values(False, 'prop').required().boolean()
        self.assertTrue(True)


class TestValidatorFieldsInterfaceUnit(unittest.TestCase):
    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_erro:
            ValidatorFieldsInterface()
        self.assertEqual(assert_erro.exception.args[0],
                         "Can't instantiate abstract class ValidatorFieldsInterface without an implementation for abstract method 'validate'")

    def test_get_validator_fields(self):
        fields_validator = fields(ValidatorFieldsInterface)
        errors_field = fields_validator[0]
        self.assertEqual(errors_field.name, 'errors')
        self.assertIsNone(errors_field.default)

        validated_data_field = fields_validator[1]
        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)


class TestDRFValidatorUnit(unittest.TestCase):
    @patch.object(Serializer, 'is_valid', return_value=True)
    @patch.object(Serializer, 'validated_data',
                  return_value={'field': 'value'}, new_callable=PropertyMock)
    def test_if_validated_data_is_set(self, mock_is_valid: MagicMock, mock_validated_data: PropertyMock):
        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        self.assertTrue(is_valid)
        self.assertEqual(validator.validated_data, {'field': 'value'})
        mock_is_valid.assert_called_once()

    @patch.object(Serializer, 'is_valid', return_value=False)
    @patch.object(Serializer, 'errors',
                  return_value={'field': ['some error']}, new_callable=PropertyMock)
    def test_if_errors_is_set(self, mock_is_valid: MagicMock, mock_validated_data: PropertyMock):
        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        self.assertFalse(is_valid)
        self.assertEqual(validator.errors, {'field': ['some error']})
        mock_is_valid.assert_called_once()
