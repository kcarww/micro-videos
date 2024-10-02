from django.urls import path

from core.category.application.use_cases import CreateCategoryUseCase
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from .api import CategoryResource 
from django_app import container #pylint: disable=E0611


class CategoryInMemoryFactory:
    repo: CategoryInMemoryRepository = None

    @classmethod
    def create(cls):
        if not cls.repo:
            cls.repo = CategoryInMemoryRepository()
        return cls.repo


class CreateCategoryUseCaseFactory:

    @staticmethod
    def create():
        repo = CategoryInMemoryFactory.create()
        return CreateCategoryUseCase(repo)


def __init_category_resource():
    return {
        'create_use_case': container.use_case_category_create_category,
        'list_use_case': container.use_case_category_list_categories,
        'get_use_case': container.use_case_category_get_category,
        'update_use_case': container.use_case_category_update_category,
        'delete_use_case': container.use_case_category_delete_category
    }


urlpatterns = [
    path('categories', CategoryResource.as_view(
        **__init_category_resource()
    )),
    path('categories/<uuid:id>', CategoryResource.as_view(
        **__init_category_resource()
    )),
]
