from typing import Callable
from rest_framework.response import Response
from rest_framework.request import Request
from core.category.application.dto import CategoryOutput
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase
)
from dataclasses import dataclass
from rest_framework.views import APIView
from rest_framework import status

from core.__seedwork.infra.django_app.serializers import UUIDSerializer
from core.category.infra.django_app.serializers import CategoryCollectionSerializer, CategorySerializer


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    def post(self, request: Request):

        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_param = CreateCategoryUseCase.Input(**serializer.validated_data)
        output = self.create_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output)
        return Response(body, status=status.HTTP_201_CREATED)

    def get(self, request: Request, id: str = None):
        if id:
            return self.get_object(id)
        input_param = ListCategoriesUseCase.Input(
            **request.query_params.dict())
        output_param = self.list_use_case().execute(input_param)
        data = CategoryCollectionSerializer(
            instance=output_param).data
        return Response(data)

    def get_object(self, id: str):
        CategoryResource.validate_id(id)
        input_param = GetCategoryUseCase.Input(id)
        output_param = self.get_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output_param)
        return Response(body)

    def put(self, request: Request, id: str):
        CategoryResource.validate_id(id)
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_param = UpdateCategoryUseCase.Input(
            **{'id': id,  **serializer.validated_data})
        output_param = self.update_use_case().execute(input_param)
        body = CategoryResource.category_to_response(output_param)
        return Response(body)

    def delete(self, _request: Request, id: str):
        CategoryResource.validate_id(id)
        input_param = DeleteCategoryUseCase.Input(id=id)
        self.delete_use_case().execute(input_param)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def category_to_response(output: CategoryOutput):
        serializer = CategorySerializer(instance=output)
        return serializer.data

    @staticmethod
    def validate_id(id: str):
        serializer = UUIDSerializer(data={'id': id})
        serializer.is_valid(raise_exception=True)
