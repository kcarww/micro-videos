import unittest
from dataclasses import dataclass
from typing import Optional
from __seedwork.domain.repositories import RepositoryInterface
from __seedwork.domain.entities import Entity
from __seedwork.domain.repositories import InMemoryRepository
from __seedwork.domain.exceptions import NotFoundException
from __seedwork.domain.value_objects import UniqueEntityId
from __seedwork.domain.repositories import SearchableRepositoryInterface, SearchParams, Filter


class TestRepositoryInterface(unittest.TestCase):
    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0], "Can't instantiate abstract class RepositoryInterface without an implementation for abstract methods 'delete', 'find_all', 'find_by_id', 'insert', 'update'")


@dataclass(slots=True, kw_only=True, frozen=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):
    repo: StubInMemoryRepository

    def setUp(self):
        self.repo = StubInMemoryRepository()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        entity = StubEntity(name="test", price=10.0)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items[0], entity)

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake_id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not using ID 'fake_id'")

        unique_entity_id = UniqueEntityId(
            'adea742e-b317-44bd-8236-5c104cb0dce3')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not using ID 'adea742e-b317-44bd-8236-5c104cb0dce3'")

    def test_find_by_id(self):
        entity = StubEntity(name="test", price=10.0)
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity)

    def test_find_all(self):
        entity = StubEntity(name="test", price=10.0)
        self.repo.insert(entity)

        entities = self.repo.find_all()
        self.assertListEqual(entities, [entity])

    def test_throw_not_found_exception_in_update(self):
        entity = StubEntity(name="test", price=10.0)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity.id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not using ID '{entity.id}'")

    def test_update(self):
        entity = StubEntity(name="test", price=10.0)
        self.repo.insert(entity)

        entity_updated = StubEntity(
            unique_entity_id=entity.unique_entity_id, name='updated', price=29.9)
        self.repo.update(entity_updated)
        self.assertEqual(self.repo.items[0], entity_updated)

    def test_throw_not_found_exception_in_delete(self):
        entity = StubEntity(name="test", price=10.0)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not using ID '{entity.id}'")

        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity.unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not using ID '{entity.id}'")

    def test_delete(self):
        entity = StubEntity(name="test", price=10.0)
        self.repo.insert(entity)
        self.repo.delete(entity.id)
        self.assertTrue(entity not in self.repo.items)


class TestSearchableRepositoryInterface(unittest.TestCase):
    def test_throw_error_when_methods_not_implemeneted(self):
        with self.assertRaises(TypeError) as assert_error:
            SearchableRepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0], "Can't instantiate abstract class SearchableRepositoryInterface without an implementation for abstract methods 'delete', 'find_all', 'find_by_id', 'insert', 'search', 'update'")


class TestSearchParams(unittest.TestCase):
    def test_props_annotations(self):
        self.assertEqual(SearchParams.__annotations__,
                         {
                             'page': Optional[int],
                             'per_page': Optional[int],
                             'sort': Optional[str],
                             'sort_dir': Optional[str],
                             'filter': Optional[Filter]
                         })

    def test_page_prop(self):
        params = SearchParams()
        arrange = [
            {'page': None, 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
            {'page': "", 'expected': 1},
            {'page': "teste", 'expected': 1},
        ]
        
        for i in arrange:
            params = SearchParams(page=i['page'])
            self.assertEqual(params.page, i['expected'])
            
    def test_per_page_prop(self):
        params = SearchParams()
        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': 1, 'expected': 1},
            {'per_page': 2, 'expected': 2},
            {'per_page': "", 'expected': 15},
            {'per_page': "teste", 'expected': 15},
            {'per_page': False, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': True, 'expected': 1},
        ]
        
        for i in arrange:
            params = SearchParams(per_page=i['per_page'])
            self.assertEqual(params.per_page, i['expected'])
    
    def test_sort_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort)
        arrange = [
            {'sort': None, 'expected': None},
            {'sort': 0, 'expected': '0'},
            {'sort': 1, 'expected': '1'},
            {'sort': 'ASC', 'expected': 'ASC'},
            {'sort': "", 'expected': None},
        ]
        
        for i in arrange:
            params = SearchParams(sort=i['sort'])
            self.assertEqual(params.sort, i['expected'])
            
    def test_sort_dir_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_dir)
        
        arrange = [
            {'sort_dir': 0, 'expected': 'asc'},
            {'sort_dir': 1, 'expected': 'asc'},
            {'sort_dir': 'ASC', 'expected': 'asc'},
            {'sort_dir': 'DESC', 'expected': 'desc'},
            {'sort_dir': 'desc', 'expected': 'desc'},
            {'sort_dir': 'asc', 'expected': 'asc'},
            {'sort_dir': "", 'expected': 'asc'},
            {'sort_dir': None, 'expected': 'asc'},
            
        ]
        for i in arrange:
            params = SearchParams(sort_dir=i['sort_dir'], sort='name')
            self.assertEqual(params.sort_dir, i['expected'])
            
    def test_filter_prop(self):
        params = SearchParams()
        self.assertIsNone(params.filter)
        arrange = [
            {'filter': None, 'expected': None},
            {'filter': 0, 'expected': '0'},
            {'filter': 1, 'expected': '1'},
            {'filter': 'ASC', 'expected': 'ASC'},
            {'filter': "", 'expected': None},
            
        ]
        
        for i in arrange:
            params = SearchParams(filter=i['filter'])
            self.assertEqual(params.filter, i['expected'])