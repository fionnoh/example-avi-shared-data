"""
GAVIP Example AVIS: Data Sharing AVI

Django models used by the AVI pipeline
"""

import datetime
from django.db import models
from pipeline.models import AviJob, AviJobRequest


class SharedDataModel(AviJob):
    """
    This model is used to store the parameters for the AVI pipeline.
    Notice that it contains identical field names here as is the variables in
    the pipeline itself.

    An AviJob model must contain all fields required by the intended
    pipeline class (ProcessVOTable) in this case.    
    """

    sharedfile = models.CharField(max_length=1000)
    outputFile = models.CharField(default="", max_length=100)
    pipeline_task = "ProcessVOTable"

    def get_absolute_url(self):
        return "%i/" % self.pk
