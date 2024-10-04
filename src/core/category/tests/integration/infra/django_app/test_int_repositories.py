import unittest

import pytest

from core.__seedwork.domain.exceptions import NotFoundException
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.infra.django_app.models import CategoryModel
from core.category.infra.django_app.repositories import CategoryDjangoRepository

@pytest.mark.django_db
class TestCategoryDjangoRepositoryInt(unittest.TestCase):
    
    repo: CategoryDjangoRepository
    
    def setUp(self):
        self.repo = CategoryDjangoRepository()
    
    
    def test_insert(self):
        category = Category(name='movie')
        self.repo.insert(category)
        
        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(category.id, str(model.id))        
        self.assertEqual(category.name, model.name)        
        self.assertEqual(category.is_active, model.is_active)        
        self.assertEqual(category.description, model.description)        
        self.assertEqual(category.created_at, model.created_at)        


    def throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake_id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake_id'")

        unique_entity_id = UniqueEntityId(
            'adea742e-b317-44bd-8236-5c104cb0dce3')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'adea742e-b317-44bd-8236-5c104cb0dce3'")


    def test_find_by_id(self):
        category = Category(
            name='Movie',
        )
        self.repo.insert(category)
        
        entity_found = self.repo.find_by_id(category.id)
        
        self.assertEqual(category, entity_found)

    def test_find_all(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_search(self):
        pass