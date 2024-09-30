from rest_framework.response import Response
from rest_framework.request import Request
from core.category.application.use_cases import (CreateCategoryUseCase,
                                                 ListCategoriesUseCase)
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from dataclasses import asdict, dataclass
from rest_framework.views import APIView


@dataclass(slots=True)
class CategoryResource(APIView):
    create_use_case: CreateCategoryUseCase

    def post(self, request: Request):
        input_param = CreateCategoryUseCase.Input(request.data['name'])
        output = self.create_use_case.execute(input_param)
        return Response(asdict(output))
    
    def get(self, request: Request):
        list_use_case = ListCategoriesUseCase(self.repo)
        input_param = ListCategoriesUseCase.Input()
        outpu_param = list_use_case.execute(input_param)
        return Response(asdict(outpu_param))





# @api_view(['POST'])
# def hello_world(request: Request):
#     create_use_case = CreateCategoryUseCase(CategoryInMemoryRepository())
#     input_param = CreateCategoryUseCase.Input(request.data['name'])
#     output_param = create_use_case.execute(input_param)
#     return Response(asdict(output_param))