"""
GAVIP Example AVIS: Data Sharing AVI

An example AVI pipeline is defined here, consisting of one task:

- ProcessData - generates HTML from a VOTable
@req: REQ-0006
@comp: AVI Web System
"""

import os
import time
import json
import logging
from django.conf import settings

import matplotlib
# Run without UI
matplotlib.use('Agg')
import numpy as np
from astropy.table import Table
import pandas_profiling
import pandas as pd

# Class used for creating pipeline tasks
from pipeline.classes import (
    AviTask,
    AviParameter, AviLocalTarget,
)

logger = logging.getLogger(__name__)


class ProcessVOTable(AviTask):
    """
    This function requires a VOTable as an input. Then we 
    present it using pandas.
    """
    sharedfile = AviParameter()
    outputFile = AviParameter()

    def output(self):
        return AviLocalTarget(os.path.join(
            settings.OUTPUT_PATH, self.outputFile
        ))

    def input(self):
        return AviLocalTarget(os.path.join(
            settings.INPUT_PATH, self.sharedfile
        ))

    def run(self):

        """
        Analyses the VOTable file containing the GACS-dev query results
        """
        logger.info('Input VOTable file: %s' % self.input().path)
        t = Table.read(self.input().path, format='votable')
        df = pd.DataFrame(np.ma.filled(t.as_array()), columns=t.colnames)

        profile = pandas_profiling.ProfileReport(df)

        analysis_context = {'gacs_dfdescription': df.describe().to_html(classes='table table-striped table-bordered table-hover'),
                            'pandas_profiling': profile.html}

        # logger.debug('analysis_context %s' % analysis_context)
        # JSON will be the context used for the template
        with open(self.output().path, 'wb') as out:
            json.dump(analysis_context, out)
