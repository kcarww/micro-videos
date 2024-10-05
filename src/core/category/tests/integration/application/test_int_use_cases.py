import unittest
import pytest

from model_bakery import baker
from core.__seedwork.domain.exceptions import NotFoundException
from core.category.application.use_cases import CreateCategoryUseCase, GetCategoryUseCase
from core.category.infra.django_app.models import CategoryModel
from core.category.infra.django_app.repositories import CategoryDjangoRepository



@pytest.mark.django_db
class TestCreateCategoryUseCaseInt(unittest.TestCase):
    use_case: CreateCategoryUseCase
    repo: CategoryDjangoRepository
    
    
    def setUp(self):
        self.repo = CategoryDjangoRepository()
        self.use_case = CreateCategoryUseCase(self.repo)
        
    def test_execute(self):
        input_param = CreateCategoryUseCase.Input(name='Category 1')
        output = self.use_case.execute(input_param)

        entity = self.repo.find_by_id(output.id)
        
        self.assertEqual(output, CreateCategoryUseCase.Output(
            id = entity.id,
            name = 'Category 1',
            description = None,
            is_active = True,
            created_at = entity.created_at
        ))
        
        self.assertEqual(entity.name, 'Category 1')
        self.assertIsNone(entity.description)
        self.assertTrue(entity.is_active)
        
        
        input_param = CreateCategoryUseCase.Input(
            name='Movie2',
            description='some description'
        )
        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)

        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=entity.id,
            name='Movie2',
            description='some description',
            is_active=True,
            created_at=entity.created_at
        ))
        self.assertEqual(entity.name, 'Movie2')
        self.assertEqual(entity.description, 'some description')
        self.assertTrue(entity.is_active)

        input_param = CreateCategoryUseCase.Input(
            name='Movie3',
            description='some description --',
            is_active=True
        )
        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)

        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=entity.id,
            name='Movie3',
            description='some description --',
            is_active=True,
            created_at=entity.created_at
        ))
        self.assertEqual(entity.name, 'Movie3')
        self.assertEqual(entity.description, 'some description --')
        self.assertTrue(entity.is_active)

        input_param = CreateCategoryUseCase.Input(
            name='Movie4',
            description='some description ##',
            is_active=False
        )
        output = self.use_case.execute(input_param)
        entity = self.repo.find_by_id(output.id)

        self.assertEqual(output, CreateCategoryUseCase.Output(
            id=entity.id,
            name='Movie4',
            description='some description ##',
            is_active=False,
            created_at=entity.created_at
        ))
        self.assertEqual(entity.name, 'Movie4')
        self.assertEqual(entity.description, 'some description ##')
        self.assertFalse(entity.is_active)
        
        
@pytest.mark.django_db
class TestGetCategoryUseCaseInt(unittest.TestCase):

    use_case: GetCategoryUseCase
    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()
        self.use_case = GetCategoryUseCase(self.repo)

    def test_throws_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input('fake id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'")

    def test_execute(self):
        entity = baker.make(CategoryModel)
        input_param = GetCategoryUseCase.Input(entity.id)
        output = self.use_case.execute(input_param)
        self.assertEqual(output, GetCategoryUseCase.Output(
            id=str(entity.id),
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at
        ))
