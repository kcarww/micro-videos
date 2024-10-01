from typing import Callable
from rest_framework.response import Response
from rest_framework.request import Request
from core.category.application.use_cases import (CreateCategoryUseCase,
                                                 ListCategoriesUseCase)
from dataclasses import asdict, dataclass, is_dataclass
from rest_framework.views import APIView
from rest_framework import status


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    def post(self, request: Request):
        input_param = CreateCategoryUseCase.Input(**request.data)
        output = self.create_use_case().execute(input_param)
        return Response(asdict(output), status=status.HTTP_201_CREATED)
    
    def get(self, request: Request):
        input_param = ListCategoriesUseCase.Input(**request.query_params.dict())        
        outpu_param = self.list_use_case().execute(input_param)
        return Response(asdict(outpu_param))





# @api_view(['POST'])
# def hello_world(request: Request):
#     create_use_case = CreateCategoryUseCase(CategoryInMemoryRepository())
#     input_param = CreateCategoryUseCase.Input(request.data['name'])
#     output_param = create_use_case.execute(input_param)
#     return Response(asdict(output_param))