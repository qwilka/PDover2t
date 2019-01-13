import logging

import numpy as np

import pdover2t
from pflacs import Loadcase, CallNode

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # logging.DEBUG 
lh = logging.StreamHandler()
logger.addHandler(lh)

vnpkl_file = "/home/develop/engineering/src/scratch/pflacs_test/pf_test.vnpkl"

basecase = Loadcase.openfile(vnpkl_file)
