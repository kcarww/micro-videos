import unittest
from typing import Optional
from unittest.mock import patch
from __seedwork.domain.exceptions import NotFoundException
from category.application.use_cases import CreateCategoryUseCase, GetCategoryUseCase
from category.domain.entities import Category
from category.infra.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):
    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository
    
    def setUp(self):
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)
        
    def test_input(self):
        self.assertEqual(CreateCategoryUseCase.Input.__annotations__, 
                         {
                             'name': str,
                             'description': Optional[str],
                             'is_active': Optional[bool]
                         })
        #pylint: disable=E1101
        description_field = CreateCategoryUseCase.Input.__dataclass_fields__['description']
        self.assertEqual(description_field.default, Category.get_field('description').default)
        
        
        is_active_field = CreateCategoryUseCase.Input.__dataclass_fields__['is_active']
        self.assertEqual(is_active_field.default, Category.get_field('is_active').default)
        
        
    def test_execute(self):
        with patch.object(self.category_repo,
                          'insert',
                          wraps=self.category_repo.insert) as spy_insert:
            input_param = CreateCategoryUseCase.Input(name='Movie')
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))
            
        input_param = CreateCategoryUseCase.Input(name='teste',
                                                  description='some')
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=self.category_repo.items[1].id,
            name='teste',
            description='some',
            is_active=True,
            created_at=self.category_repo.items[1].created_at
        ))
        
        input_param = CreateCategoryUseCase.Input(name='teste',
                                                  description='some',
                                                  is_active=False)
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=self.category_repo.items[2].id,
            name='teste',
            description='some',
            is_active=False,
            created_at=self.category_repo.items[2].created_at
        ))
        
        
        
class TestGetCategoryUseCaseUnit(unittest.TestCase):
    use_case: GetCategoryUseCase
    category_repo: CategoryInMemoryRepository
    
    def setUp(self):
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)
        
    def test_input(self):
        self.assertEqual(GetCategoryUseCase.Input.__annotations__, 
                         {
                             'id': str
                         })

    def test_throw_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input('fake id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(assert_error.exception.args[0], f"Entity not found using ID '{input_param.id}'")
            
        
    def test_execute(self):
        category = Category(name='Movie')
        self.category_repo.items = [category]
        with patch.object(self.category_repo,
                          'find_by_id',
                          wraps=self.category_repo.find_by_id) as spy_find_by_id:
            input_param = GetCategoryUseCase.Input(id=category.id)
            output = self.use_case.execute(input_param)
            spy_find_by_id.assert_called_once()
            self.assertEqual(output, GetCategoryUseCase.Output(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))
            
        