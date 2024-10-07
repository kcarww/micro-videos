
import pytest
from django.forms import ValidationError
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.utils import timezone
from core.category.application.dto import CategoryOutput
from core.category.infra.django_app.api import CategoryResource

from django_app import container
from core.category.tests.helpers import init_category_resource_all_none


@pytest.mark.django_db
class TestCategoryResourceCommonMethodsInt:
    resource: CategoryResource

    @classmethod
    def setup_class(cls):

        cls.resource = CategoryResource(
            **{
                **init_category_resource_all_none(),
                'create_use_case': container.use_case_category_create_category,
            }
        )

    def test_category_to_response(self):
        output = CategoryOutput(
            id='fake id',
            name='category test',
            description='description teste',
            is_active=True,
            created_at=timezone.now()
        )

        data = CategoryResource.category_to_response(output)
        assert data == {
            'id': 'fake id',
            'name': 'category test',
            'description': 'description teste',
            'is_active': True,
            'created_at': f'{output.created_at.isoformat()[:-6]}Z'
        }

    def test_validate_id(self):
        with pytest.raises(ValidationError)as assert_exception:
            CategoryResource.validate_id('fake id')
        print(assert_exception, '---------------')

        expected_error = {
            'id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
        }
        assert assert_exception.value.detail == expected_error
