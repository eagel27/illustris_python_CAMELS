"""Tests for the `illustris_python.groupcat` submodule.

Running Tests
-------------
To run all tests, this script can be executed as:
    `$ python tests/groupcat_test.py [-v] [--nocapture]`
from the root directory.

Alternatively, `nosetests` can be run and it will find the tests:
    `$ nosetests [-v] [--nocapture]`

To run particular tests (for example),
    `$ nosetests tests/groupcat_test.py:test_groupcat_loadSubhalos`

To include coverage information,
    `$ nosetests --with-coverage --cover-package=.`

"""

import os

from nose.tools import assert_true, assert_equal, assert_raises
import numpy as np

# `illustris_python` is imported as `ill` in local `__init__.py`
from . import ill, BASE_PATH_CAMELS_TNG


# =========================
# ====    loadHalos    ====
# =========================


def test_groupcat_loadHalos_field():
    fields = ['GroupFirstSub']
    snap = 33
    group_first_sub = ill.groupcat.loadHalos(BASE_PATH_CAMELS_TNG, snap, fields=fields)
    print("group_first_sub.shape = ", group_first_sub.shape)
    assert_equal(group_first_sub.shape, (20817,))
    print("group_first_sub = ", group_first_sub)
    assert_true(np.all(group_first_sub[:3] == [0, 505, 593]))
    return


def test_groupcat_loadHalos_all_fields():
    snap = 33
    num_fields = 26
    # Values for CAMELS_TNG_1P_1_0, snap 33
    cat_shape = (20817,)
    first_key = 'GroupBHMass'
    all_fields = ill.groupcat.loadHalos(BASE_PATH_CAMELS_TNG, snap)
    print("len(all_fields.keys()) = {} (should be {})".format(len(all_fields.keys()), num_fields))
    assert_equal(len(all_fields.keys()), num_fields)
    key = sorted(all_fields.keys())[0]
    print("all_fields.keys()[0] = '{}' (should be '{}')".format(key, first_key))
    assert_equal(key, first_key)
    shape = np.shape(all_fields[key])
    print("np.shape(all_fields[{}]) = {} (should be {})".format(
        key, shape, cat_shape))
    assert_equal(shape, cat_shape)
    return


def test_groupcat_loadHalos_1():
    fields = ['GroupFirstSub']
    snap = 33
    # Construct a path that should not be found: fail
    fail_path = os.path.join(BASE_PATH_CAMELS_TNG, 'failure')
    print("path '{}' should not be found".format(fail_path))
    # `OSError` is raised in python3 (but in py3 OSError == IOError), `IOError` in python2
    assert_raises(IOError, ill.groupcat.loadHalos, fail_path, snap, fields=fields)
    return


def test_groupcat_loadHalos_2():
    fields = ['GroupFirstSub']
    snap = 34
    # Construct a path that should not be found: fail
    print("snap '{}' should not be found".format(snap))
    # `OSError` is raised in python3 (but in py3 OSError == IOError), `IOError` in python2
    assert_raises(IOError, ill.groupcat.loadHalos, BASE_PATH_CAMELS_TNG, snap, fields=fields)
    return


def test_groupcat_loadHalos_3():
    # This field should not be found
    fields = ['GroupFailSub']
    snap = 33
    # Construct a path that should not be found: fail
    print("fields '{}' should not be found".format(fields))
    assert_raises(Exception, ill.groupcat.loadHalos, BASE_PATH_CAMELS_TNG, snap, fields=fields)
    return


# ==========================
# ====    loadSingle    ====
# ==========================


def test_groupcat_loadSingle():
    # Gas fractions for the first 5 subhalos
    gas_frac = [0.17558935, 0.0, 0.41750327, 0.0014895789, 0.0]

    ptNumGas = ill.snapshot.partTypeNum('gas')  # 0
    ptNumStars = ill.snapshot.partTypeNum('stars')  # 4
    for i in range(5):
        # all_fields = ill.groupcat.loadSingle(BASE_PATH_ILLUSTRIS_1, 135, subhaloID=group_first_sub[i])
        all_fields = ill.groupcat.loadSingle(BASE_PATH_CAMELS_TNG, 33, subhaloID=i)
        gas_mass   = all_fields['SubhaloMassInHalfRadType'][ptNumGas]
        stars_mass = all_fields['SubhaloMassInHalfRadType'][ptNumStars]
        frac = gas_mass / (gas_mass + stars_mass)
        # print(i, group_first_sub[i], frac)
        print("subhalo {} with gas frac '{}' (should be '{}')".format(i, frac, gas_frac[i]))
        assert_true(np.isclose(frac, gas_frac[i]))

    return


# ============================
# ====    loadSubhalos    ====
# ============================


def test_groupcat_loadSubhalos():
    fields = ['SubhaloMass', 'SubhaloSFRinRad']
    snap = 33
    subhalos = ill.groupcat.loadSubhalos(BASE_PATH_CAMELS_TNG, snap, fields=fields)
    print("subhalos['SubhaloMass'] = ", subhalos['SubhaloMass'].shape)
    assert_true(subhalos['SubhaloMass'].shape == (18635,))
    print("subhalos['SubhaloMass'] = ", subhalos['SubhaloMass'])
    assert_true(
        np.allclose(subhalos['SubhaloMass'][:3], [8798.259, 50.36114, 46.977165]))
    return
