from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

class Test(APIView):

    def get(self, request):
        return Response({"message":"Удачная проверка"})

# Create your views here.
