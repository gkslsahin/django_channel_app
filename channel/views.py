from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict

from .models import Channel


class ModelViewSet(APIView):
    def get(self, request, format=None):
        query_result = Channel.objects.all()
        result_dict = {}
        for result in query_result:
            all_child = result.get_all_children()
            result_dict[str(result)] = []
            for child in all_child:
                result_dict[str(result)].append(model_to_dict(child))
        return Response(result_dict)
