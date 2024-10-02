from typing import Callable
from rest_framework.response import Response
from rest_framework.request import Request
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase
)
from dataclasses import asdict, dataclass
from rest_framework.views import APIView
from rest_framework import status


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    def post(self, request: Request):
        input_param = CreateCategoryUseCase.Input(**request.data)
        output = self.create_use_case().execute(input_param)
        return Response(asdict(output), status=status.HTTP_201_CREATED)

    def get(self, request: Request, id: str = None):
        if id:
            return self.get_object(id)
        input_param = ListCategoriesUseCase.Input(
            **request.query_params.dict())
        outpu_param = self.list_use_case().execute(input_param)
        return Response(asdict(outpu_param))

    def get_object(self, id: str):
        input_param = GetCategoryUseCase.Input(id)
        output_param = self.get_use_case().execute(input_param)
        return Response(asdict(output_param))

    def put(self, request: Request, id: str):
        input_param = UpdateCategoryUseCase.Input(
            **{'id': id,  **request.data})
        output_param = self.update_use_case().execute(input_param)
        return Response(asdict(output_param))

    def delete(self, id: str):
        input_param = DeleteCategoryUseCase.Input(id)
        output_param = self.delete_use_case().execute(input_param)
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['POST'])
# def hello_world(request: Request):
#     create_use_case = CreateCategoryUseCase(CategoryInMemoryRepository())
#     input_param = CreateCategoryUseCase.Input(request.data['name'])
#     output_param = create_use_case.execute(input_param)
#     return Response(asdict(output_param))
