from django.urls import path

from core.category.application.use_cases import CreateCategoryUseCase
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from .api import CategoryResource


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

urlpatterns = [
    path('categories', CategoryResource.as_view(create_use_case=CreateCategoryUseCaseFactory.create())),
]
