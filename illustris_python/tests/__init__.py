"""Tests.
"""

import os
import sys

SIM_DIR = '1P_1_0'
BASE_PATH_CAMELS_TNG = '/home/jovyan/PUBLIC_RELEASE/Sims/IllustrisTNG/{}/'.format(SIM_DIR)

# Add path to directory containing 'illustris_python' module
#    e.g. if this file is in '/n/home00/lkelley/illustris/illustris_python/tests/'
this_path = os.path.realpath(__file__)
ill_py_path = os.path.abspath(os.path.join(this_path, os.path.pardir, os.path.pardir, os.path.pardir))
sys.path.append(ill_py_path)
import illustris_python as ill
