from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, AdminRenderer

from django.shortcuts import get_object_or_404
from django.conf import settings

from pipeline import manager
from avi.models import SharedDataModel
from avi.serializers import SharedDataModelSerializer, ViewJobsSerializer

import os
import json
import logging
logger = logging.getLogger(__name__)


class SharedDataModelList(generics.ListCreateAPIView):
    queryset = SharedDataModel.objects.all()
    serializer_class = SharedDataModelSerializer
    renderer_classes = (JSONRenderer, AdminRenderer)


class SharedDataModelDetail(generics.RetrieveDestroyAPIView):
    queryset = SharedDataModel.objects.all()
    serializer_class = SharedDataModelSerializer
    renderer_classes = (JSONRenderer, AdminRenderer)


class JobData(APIView):

    def get(self, request, job_id):
        job = get_object_or_404(SharedDataModel, request_id=job_id)
        file_path = os.path.join(settings.OUTPUT_PATH, job.outputFile)
        with open(file_path, 'r') as outFile:
            job_data = json.load(outFile)
        return Response(job_data)


class ViewJobsList(generics.ListAPIView):
    queryset = SharedDataModel.objects.all()
    serializer_class = ViewJobsSerializer
    renderer_classes = (JSONRenderer, AdminRenderer)


class ViewJobsListDetail(generics.RetrieveAPIView):
    queryset = SharedDataModel.objects.all()
    serializer_class = ViewJobsSerializer
    renderer_classes = (JSONRenderer, AdminRenderer)
