import unittest

import pytest

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

    def test_find_by_id(self):
        pass

    def test_find_all(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_search(self):
        pass