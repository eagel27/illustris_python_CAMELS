"""Tests for the `illustris_python.sublink` submodule.

Running Tests
-------------
To run all tests, this script can be executed as:
    `$ python tests/sublink_test.py [-v] [--nocapture]`
from the root directory.

Alternatively, `nosetests` can be run and it will find the tests:
    `$ nosetests [-v] [--nocapture]`

To run particular tests (for example),
    `$ nosetests tests/sublink_test.py:test_loadTree`

To include coverage information,
    `$ nosetests --with-coverage --cover-package=.`

"""
import os
import glob
import numpy as np
from nose.tools import assert_equal, assert_raises, assert_true, assert_false

# `illustris_python` is imported as `ill` in local `__init__.py`
from . import ill, BASE_PATH_CAMELS_TNG


def test_treePath_1():
    tree_name = "SubLink"
    _path = ill.sublink.treePath(BASE_PATH_CAMELS_TNG, tree_name, '*')
    paths = glob.glob(_path)
    assert_false(len(paths) == 0)
    assert_true(os.path.exists(paths[0]))
    return


def test_treePath_2():
    # Construct a path that should fail
    tree_name = "SubLinkFail"
    assert_raises(ValueError, ill.sublink.treePath, BASE_PATH_CAMELS_TNG, tree_name, '*')
    return


def test_loadTree():
    fields = ['SubhaloMass', 'SubfindID', 'SnapNum']
    snap = 33
    start = 100

    # Values for CAMELS_TNG_1P_1_0, snap=33, start=100
    snap_num_last = [0, 2, 0, 0, 2]
    subhalo_mass_last = [0.6902156, 1.5663164, 0.5560228, 0.93303096, 1.8127693]

    group_first_sub = ill.groupcat.loadHalos(BASE_PATH_CAMELS_TNG, snap, fields=['GroupFirstSub'])

    for ii, nn, mm in zip(range(start, start+5), snap_num_last, subhalo_mass_last):
        tree = ill.sublink.loadTree(
            BASE_PATH_CAMELS_TNG, snap, group_first_sub[ii], fields=fields, onlyMPB=True)
        assert_equal(tree['SnapNum'][-1], nn)
        assert_true(np.isclose(tree['SubhaloMass'][-1], mm))

    return


def test_numMergers():
    snap = 33
    ratio = 1.0/5.0
    start = 100

    # Values for CAMELS_TNG_1P_1_0, snap=33, start=100
    num_mergers = [1, 3, 3, 1, 3]

    group_first_sub = ill.groupcat.loadHalos(BASE_PATH_CAMELS_TNG, snap, fields=['GroupFirstSub'])

    # the following fields are required for the walk and the mass ratio analysis
    fields = ['SubhaloID', 'NextProgenitorID', 'MainLeafProgenitorID',
              'FirstProgenitorID', 'SubhaloMassType']
    for i, nm in zip(range(start, start+5), num_mergers):
        tree = ill.sublink.loadTree(BASE_PATH_CAMELS_TNG, snap, group_first_sub[i], fields=fields)
        _num_merg = ill.sublink.numMergers(tree, minMassRatio=ratio)
        print("group_first_sub[{}] = {}, num_mergers = {} (should be {})".format(
            i, group_first_sub[i], _num_merg, nm))
        assert_equal(_num_merg, nm)

    return
