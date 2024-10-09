
from dataclasses import dataclass
from typing import Any, Optional
from rest_framework.exceptions import ErrorDetail, ValidationError
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
    response: Optional[Response] = None
    exception: Optional[Exception] = None



@dataclass
class CategoryInvalidBodyFixture:
    body_empty: HttpExpect
    name_none: HttpExpect
    name_empty: HttpExpect
    name_not_a_str: HttpExpect
    description_not_a_str: HttpExpect
    is_active_none: HttpExpect
    is_active_empty: HttpExpect
    is_active_not_a_bool: HttpExpect

    @staticmethod
    def arrange():
        faker = Category.fake().a_category()
        return CategoryInvalidBodyFixture(
            body_empty=HttpExpect(
                request=Request(body={}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                })
            ),
            name_none=HttpExpect(  # vai acontecer um erro
                request=Request(
                    body={'name': faker.with_invalid_name_none().name}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field may not be null.', 'null')
                    ],
                })),
            name_empty=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_empty().name}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field may not be blank.', 'blank')
                    ],
                })),
            name_not_a_str=HttpExpect(
                request=Request(
                    body={'name': faker.with_invalid_name_not_a_string().name}),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('Not a valid string', 'invalid')
                    ],
                })),
            description_not_a_str=HttpExpect(
                request=Request(
                    body={
                        'description': faker.with_invalid_description_not_a_string().description
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'description': [
                        ErrorDetail('Not a valid string', 'invalid')
                    ],
                })),
            is_active_none=HttpExpect(
                request=Request(
                    body={
                        'is_active': faker.with_invalid_is_active_none().is_active
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'is_active': [
                        ErrorDetail('This field may not be null.', 'null')
                    ],
                })),
            is_active_empty=HttpExpect(
                request=Request(
                    body={
                        'is_active': faker.with_invalid_is_active_empty().is_active
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'is_active': [
                        ErrorDetail('Must be a valid boolean.', 'invalid')
                    ],
                })),
            is_active_not_a_bool=HttpExpect(
                request=Request(
                    body={
                        'is_active': faker.with_invalid_is_active_not_a_boolean().is_active
                    }
                ),
                exception=ValidationError({
                    'name': [
                        ErrorDetail('This field is required.', 'required')
                    ],
                    'is_active': [
                        ErrorDetail('Must be a valid boolean.', 'invalid')
                    ],
                })),
        )


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
