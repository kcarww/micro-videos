from datetime import datetime
import unittest
from unittest import mock
from core.category.application.dto import CategoryOutput
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)
from core.category.infra.django_app.api import CategoryResource
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from core.category.infra.django_app.serializers import CategorySerializer


class StubCategorySerializer:
    validated_data = None

    def is_valid(self, raise_exception: bool):
        pass


class TestCategoryResourceUnit(unittest.TestCase):
    
    def test_post_method(self):
        stub_serializer = StubCategorySerializer()
        send_data = {'name': 'movie'}

        with mock.patch.object(CategorySerializer, '__new__', return_value=stub_serializer) as mock_serializer:
            stub_serializer.validated_data = send_data
            stub_serializer.is_valid = mock.MagicMock()
            
            mock_create_use_case = mock.Mock(CreateCategoryUseCase)
            mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
                id='c31d3c48-9a2d-42d0-9c5f-400249e5556b',
                name='movie',
                description=None,
                is_active=True,
                created_at=datetime.now()
            )

            resource = CategoryResource(
                **{
                    **self.__init_all_none(),
                    'create_use_case': lambda: mock_create_use_case
                }
            )

            _request = APIRequestFactory().post('/', send_data)
            request = Request(_request)
            request._full_data = send_data
            response = resource.post(request)
            stub_serializer.is_valid.assert_called_with(raise_exception=True)
            mock_create_use_case.execute.assert_called_with(CreateCategoryUseCase.Input(
                name='movie'
            ))
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data, {
                'id': 'c31d3c48-9a2d-42d0-9c5f-400249e5556b',
                'name': 'movie',
                'description': None,
                'is_active': True,
                'created_at': mock_create_use_case.execute.return_value.created_at
            })
        mock_serializer.assert_called_with(CategorySerializer, data=send_data)

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

    def test_if_get_invoke_get_object(self):
        resource = CategoryResource(**self.__init_all_none())
        resource.get_object = mock.Mock()
        resource.get(None, 'af46842e-027d-4c91-b259-3a3642144ba4')
        resource.get_object.assert_called_with(
            'af46842e-027d-4c91-b259-3a3642144ba4')

    def test_get_object__method(self):
        mock_get_use_case = mock.Mock(GetCategoryUseCase)

        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id='c31d3c48-9a2d-42d0-9c5f-400249e5556b',
            name='movie',
            description=None,
            is_active=True,
            created_at=datetime.now()
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'get_use_case': lambda: mock_get_use_case
            }
        )

        response = resource.get_object('c31d3c48-9a2d-42d0-9c5f-400249e5556b')
        mock_get_use_case.execute.assert_called_with(GetCategoryUseCase.Input(
            id='c31d3c48-9a2d-42d0-9c5f-400249e5556b'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': 'c31d3c48-9a2d-42d0-9c5f-400249e5556b',
                                         'name': 'movie',
                                         'description': None,
                                         'is_active': True,
                                         'created_at': mock_get_use_case.execute.return_value.created_at})

    def test_put__method(self):
        send_data = {
            'id': 'c31d3c48-9a2d-42d0-9c5f-400249e5556b',
            'name': 'movie'
        }
        mock_put_use_case = mock.Mock(UpdateCategoryUseCase)

        mock_put_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id=send_data['id'],
            name=send_data['name'],
            description=None,
            is_active=True,
            created_at=datetime.now()
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'update_use_case': lambda: mock_put_use_case
            }
        )
        _request = APIRequestFactory().put('/', send_data)
        request = Request(_request)
        request._full_data = send_data
        response = resource.put(
            request, send_data['id'])
        mock_put_use_case.execute.assert_called_with(UpdateCategoryUseCase.Input(
            id=send_data['id'],
            name=send_data['name']
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': send_data['id'],
                                         'name': send_data['name'],
                                         'description': None,
                                         'is_active': True,
                                         'created_at': mock_put_use_case.execute.return_value.created_at})

    def test_delete_object__method(self):
        mock_delete_use_case = mock.Mock(DeleteCategoryUseCase)

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'delete_use_case': lambda: mock_delete_use_case
            }
        )
        _request = APIRequestFactory().delete('/')
        request = Request(_request)
        response = resource.delete(
            request, 'c31d3c48-9a2d-42d0-9c5f-400249e5556b')
        mock_delete_use_case.execute.assert_called_with(DeleteCategoryUseCase.Input(
            id='c31d3c48-9a2d-42d0-9c5f-400249e5556b'
        ))
        self.assertEqual(response.status_code, 204)

    def __init_all_none(self):
        return {
            'list_use_case': None,
            'create_use_case': None,
            'get_use_case': None,
            'update_use_case': None,
            'delete_use_case': None
        }
