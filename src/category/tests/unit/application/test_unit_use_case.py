import unittest
from datetime import timedelta
from typing import Optional
from unittest.mock import patch
from django.utils import timezone
from __seedwork.application.use_cases import UseCase
from __seedwork.domain.exceptions import NotFoundException
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.application.use_cases import CreateCategoryUseCase, GetCategoryUseCase, ListCategoriesUseCase
from category.domain.entities import Category
from category.infra.repositories import CategoryInMemoryRepository


class TestCreateCategoryUseCaseUnit(unittest.TestCase):
    use_case: CreateCategoryUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self):
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(CreateCategoryUseCase.Input.__annotations__,
                         {
                             'name': str,
                             'description': Optional[str],
                             'is_active': Optional[bool]
                         })
        # pylint: disable=E1101
        description_field = CreateCategoryUseCase.Input.__dataclass_fields__[
            'description']
        self.assertEqual(description_field.default,
                         Category.get_field('description').default)

        is_active_field = CreateCategoryUseCase.Input.__dataclass_fields__[
            'is_active']
        self.assertEqual(is_active_field.default,
                         Category.get_field('is_active').default)

    def test_execute(self):
        with patch.object(self.category_repo,
                          'insert',
                          wraps=self.category_repo.insert) as spy_insert:
            input_param = CreateCategoryUseCase.Input(name='Movie')
            output = self.use_case.execute(input_param)
            spy_insert.assert_called_once()
            self.assertEqual(output, CategoryOutput(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))

        input_param = CreateCategoryUseCase.Input(name='teste',
                                                  description='some')
        output = self.use_case.execute(input_param)
        self.assertEqual(output, CategoryOutput(
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
        self.assertEqual(output, CategoryOutput(
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

    def test_if_instance_a_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_input(self):
        self.assertEqual(GetCategoryUseCase.Input.__annotations__,
                         {
                             'id': str
                         })

    def test_throw_exception_when_category_not_found(self):
        input_param = GetCategoryUseCase.Input('fake id')
        with self.assertRaises(NotFoundException) as assert_error:
            self.use_case.execute(input_param)
        self.assertEqual(assert_error.exception.args[0], f"Entity not found using ID '{
                         input_param.id}'")

    def test_execute(self):
        category = Category(name='Movie')
        self.category_repo.items = [category]
        with patch.object(self.category_repo,
                          'find_by_id',
                          wraps=self.category_repo.find_by_id) as spy_find_by_id:
            input_param = GetCategoryUseCase.Input(id=category.id)
            output = self.use_case.execute(input_param)
            spy_find_by_id.assert_called_once()
            self.assertEqual(output, CategoryOutput(
                id=self.category_repo.items[0].id,
                name='Movie',
                description=None,
                is_active=True,
                created_at=self.category_repo.items[0].created_at
            ))


class TestListCategoriesUseCaseUnit(unittest.TestCase):

    use_case: ListCategoriesUseCase
    category_repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = ListCategoriesUseCase(self.category_repo)

    def test_instance_use_case(self):
        self.assertIsInstance(self.use_case, UseCase)

    def test_execute_using_empty_search_params(self):
        self.category_repo.items = [
            Category(name='test 1'),
            Category(name='test 2', created_at=timezone.now() +
                     timedelta(seconds=200)),
        ]
        with patch.object(self.category_repo, 'search', wraps=self.category_repo.search) as spy_search:
            input_param = ListCategoriesUseCase.Input()
            output = self.use_case.execute(input_param)
            spy_search.assert_called_once()
            self.assertEqual(output, ListCategoriesUseCase.Output(
                items=list(
                    map(
                        CategoryOutputMapper.to_output,
                        self.category_repo.items[::-1]
                    )
                ),
                total=2,
                current_page=1,
                per_page=15,
                last_page=1
            ))

    def test_execute_using_pagination_and_sort_and_filter(self):
        items = [
            Category(name='a'),
            Category(name='AAA'),  # asci
            Category(name='AaA'),
            Category(name='b'),
            Category(name='c'),
        ]
        self.category_repo.items = items

        input_param = ListCategoriesUseCase.Input(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.to_output, [items[1], items[2]]
                )
            ),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))
        
        input_param = ListCategoriesUseCase.Input(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.to_output, [items[0]]
                )
            ),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))
        
        input_param = ListCategoriesUseCase.Input(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='desc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.to_output, [items[0], items[2]]
                )
            ),
            total=3,
            current_page=1,
            per_page=2,
            last_page=2
        ))

        input_param = ListCategoriesUseCase.Input(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='desc',
            filter='a'
        )
        output = self.use_case.execute(input_param)
        self.assertEqual(output, ListCategoriesUseCase.Output(
            items=list(
                map(
                    CategoryOutputMapper.to_output, [items[1]]
                )
            ),
            total=3,
            current_page=2,
            per_page=2,
            last_page=2
        ))