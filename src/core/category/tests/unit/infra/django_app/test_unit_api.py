from datetime import datetime
import unittest
from unittest import mock
from core.category.application.dto import CategoryOutput
from core.category.application.use_cases import CreateCategoryUseCase, ListCategoriesUseCase
from core.category.infra.django_app.api import CategoryResource
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request


class TestCategoryResourceUnit(unittest.TestCase):
    def test_post_method(self):
        mock_create_use_case = mock.Mock(CreateCategoryUseCase)

        send_data = {'name': 'movie'}

        create_at = datetime.now()
        mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id='c31d3c48-9a2d-42d0-9c5f-400249e5556b',
            name='movie',
            description=None,
            is_active=True,
            created_at=create_at
        )

        resource = CategoryResource(
            **{
                **self.__init__all_none(),
                'create_use_case': lambda: mock_create_use_case
            }
        )

        _request = APIRequestFactory().post('/', send_data)
        request = Request(_request)
        request._full_data = send_data
        response = resource.post(request)
        mock_create_use_case.execute.assert_called_with(CreateCategoryUseCase.Input(
            name='movie'
        ))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'id': 'c31d3c48-9a2d-42d0-9c5f-400249e5556b',
                                         'name': 'movie',
                                         'description': None,
                                         'is_active': True,
                                         'created_at': create_at})

    def test_get_method(self):
        mock_list_use_case = mock.Mock(CreateCategoryUseCase)

        mock_list_use_case.execute.return_value = ListCategoriesUseCase.Output(
            items=[
                CategoryOutput(
                    id='c31d3c48-9a2d-42d0-9c5f-400249e5556b',
                    name='movie',
                    description=None,
                    is_active=True,
                    created_at=datetime.now()
                )
            ],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'list_use_case': lambda: mock_list_use_case,
            }
        )

        _request = APIRequestFactory().get(
            '/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test')
        request = Request(_request)
        response = resource.get(request)
        mock_list_use_case.execute.assert_called_with(ListCategoriesUseCase.Input(
            page='1',
            per_page='1',
            sort='name',
            sort_dir='asc',
            filter='test'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'items': [
                {
                    'id': 'c31d3c48-9a2d-42d0-9c5f-400249e5556b',
                    'name': 'movie',
                    'description': None,
                    'is_active': True,
                    'created_at': mock_list_use_case.execute.return_value.items[0].created_at
                },

            ],
            'total': 1,
            'current_page': 1,
            'last_page': 1,
            'per_page': 2
        })

    def __init_all_none(self):
        return {
            'list_use_case': None,
            'create_use_case': None
        }
