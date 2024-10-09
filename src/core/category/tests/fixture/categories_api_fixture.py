
from dataclasses import dataclass
from typing import Any

import pytest

from core.category.domain.entities import Category


@dataclass
class Request:
    body: Any


@dataclass
class Response:
    body: Any


@dataclass
class HttpExpect:
    request: Request
    response: Response


class CategoryApiFixture:

    @staticmethod
    def keys_in_category_response():
        return [
            'id',
            'name',
            'description',
            'is_active',
            'created_at'
        ]

    @staticmethod
    def arrange_for_save():
        faker = Category.fake().a_category()\
            .with_name('Movie')\
            .with_description('description test')

        data = [
            HttpExpect(
                request=Request(body={'name': faker.name}),
                response=Response(body={
                    'name': faker.name,
                    'description': None,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={
                    'name': faker.name,
                    'description': faker.description,
                }),
                response=Response(body={
                    'name': faker.name,
                    'description': faker.description,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={
                    'name': faker.name,
                    'is_active': True
                }),
                response=Response(body={
                    'name': faker.name,
                    'description': None,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={
                    'name': faker.name,
                    'is_active': False
                }),
                response=Response(body={
                    'name': faker.name,
                    'description': None,
                    'is_active': False,
                })
            )
        ]
        return [pytest.param(item, id=str(item.request.body)) for item in data]
