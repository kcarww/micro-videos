from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import unittest
from unittest.mock import patch
from __seedwork.domain.exceptions import InvalidUuidException
from __seedwork.domain.value_objects import UniqueEntityId, ValueObject
import uuid


@dataclass(frozen=True)
class StubOneProb(ValueObject):
    prop: str
    
@dataclass(frozen=True)
class StubTwoProb(ValueObject):
    prop1: str
    prop2: str

class TestValueObjectUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))
        
    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)
        
    def test_init_prop(self):
        value_object = StubOneProb(prop='prop-value')
        self.assertEqual(value_object.prop, 'prop-value')
        
        value_object = StubTwoProb(prop1='prop1-value', prop2='prop2-value')
        self.assertEqual(value_object.prop1, 'prop1-value')
        self.assertEqual(value_object.prop2, 'prop2-value')
        
    def test_if_convert_to_string(self):
        value_object = StubOneProb(prop='prop-value')
        self.assertEqual(value_object.prop, str(value_object))
        
        value_object = StubTwoProb(prop1='prop1-value', prop2='prop2-value')
        self.assertEqual('{"prop1": "prop1-value", "prop2": "prop2-value"}', str(value_object))

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = StubOneProb(prop='value')
            value_object.prop = 'value 2'
       
class TestUniqueIdentityIdUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))
    
    def test_throw_exception_if_invalid_uuid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId('invalid-uuid')
            mock_validate.assert_called_once()
            self.assertEqual(assert_error.exception.args[0], 'Invalid UUID')
            
    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id, 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
            
        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))
        
    def test_generate_uuid_if_not_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()
            
    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = 'new-uuid'
            
    def test_convert_to_str(self):
        value_object = UniqueEntityId()
        self.assertEqual(value_object.id, str(value_object))

        
        
    