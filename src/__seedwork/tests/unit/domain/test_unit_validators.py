import unittest
from __seedwork.domain.exceptions import ValidationException
from __seedwork.domain.validators import ValidatorRules


class TestValidatorRules(unittest.TestCase):
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
