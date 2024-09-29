from abc import ABC
from dataclasses import dataclass, is_dataclass
import unittest

from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestUnitEntity(unittest.TestCase):
    def test_if_is_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_unique_entity_id_and_props(self):
        entity = StubEntity(prop1='value 1', prop2='value 2')
        self.assertEqual(entity.prop1, 'value 1')
        self.assertEqual(entity.prop2, 'value 2')
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_if_accept_valid_uuid(self):
        entity = StubEntity(unique_entity_id=UniqueEntityId('adea742e-b317-44bd-8236-5c104cb0dce3'),
                            prop1='value 1', prop2='value 2')

        self.assertEqual(entity.id, 'adea742e-b317-44bd-8236-5c104cb0dce3')

    def test_to_dict_method(self):
        entity = StubEntity(unique_entity_id=UniqueEntityId('adea742e-b317-44bd-8236-5c104cb0dce3'),
                            prop1='value 1', prop2='value 2')
        self.assertDictEqual(entity.to_dict(), {
                             'id': 'adea742e-b317-44bd-8236-5c104cb0dce3', 'prop1': 'value 1', 'prop2': 'value 2'})

    def test_set_method(self):
        entity = StubEntity(prop1='value 1', prop2='value 2')
        # pylint : disable=protected-access
        entity._set('prop1', 'new value')
        self.assertEqual(entity.prop1, 'new value')
