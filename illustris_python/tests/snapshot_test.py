"""Tests for the `illustris_python.snapshot` submodule.

Running Tests
-------------
To run all tests, this script can be executed as:
    `$ python tests/snapshot_test.py [-v] [--nocapture]`
from the root directory.

Alternatively, `nosetests` can be run and it will find the tests:
    `$ nosetests [-v] [--nocapture]`

To run particular tests (for example),
    `$ nosetests tests/snapshot_test.py:test_snapshot_partTypeNum_1`

To include coverage information,
    `$ nosetests --with-coverage --cover-package=.`

"""
import numpy as np
from nose.tools import assert_equal, assert_raises, assert_true

# `illustris_python` is imported as `ill` in local `__init__.py`
from . import ill, BASE_PATH_CAMELS_TNG


def test_snapshot_partTypeNum_1():
    names = ['gas', 'dm', 'tracers', 'stars', 'blackhole', 'GaS', 'blackholes']
    nums = [0, 1, 3, 4, 5, 0, 5]

    for name, num in zip(names, nums):
        pn = ill.snapshot.partTypeNum(name)
        print("\npartTypeNum('{}') = '{}' (should be '{}')".format(name, pn, num))
        assert_equal(pn, num)

    return


def test_snapshot_partTypeNum_2():
    # These should fail and raise an exception
    names = ['peanuts', 'monkeys']
    nums = [0, 1]

    for name, num in zip(names, nums):
        print("\npartTypeNum('{}') should raise `Exception`".format(name))
        assert_raises(Exception, ill.snapshot.partTypeNum, name)

    return


'''
# Too slow
def test_loadSubset():
    from datetime import datetime
    snap = 135
    fields = ['Masses']
    beg = datetime.now()
    gas_mass = ill.snapshot.loadSubset(BASE_PATH_ILLUSTRIS_1, snap, 'gas', fields=fields)
    print("Loaded after '{}'".format(datetime.now() - beg))
    print(np.shape(gas_mass))
    print(np.log10(np.mean(gas_mass, dtype='double')*1e10/0.704))
    return
'''


def test_loadHalo():
    snap = 33
    halo_num = 100

    # Values for CAMELS_TNG_1P_1_0, snap=33, halo 100
    coords = [[18927.308004202096, 19071.693153209173],
              [21020.63007427272, 21429.035218396126],
              [23386.91529889961, 23656.211157049107]]
    stars_count = 1594

    stars = ill.snapshot.loadHalo(BASE_PATH_CAMELS_TNG, snap, halo_num, 'stars')
    assert_equal(stars["count"], stars_count)
    for i in range(3):
        _min = np.min(stars['Coordinates'][:, i])
        _max = np.max(stars['Coordinates'][:, i])
        print("Coords axis '{}' min, max: {}, {} (should be {}, {})".format(
            i, _min, _max, coords[i][0], coords[i][1]))
        assert_true(np.isclose(_min, coords[i][0]))
        assert_true(np.isclose(_max, coords[i][1]))

    return
