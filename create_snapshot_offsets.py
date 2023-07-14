import os
import sys

import numpy as np
import h5py
import tqdm
from itertools import repeat
from multiprocessing import Pool

import illustris_python as il


def create_offsets(base_path, offsets_path, snapshot):
    """
    Calculate offsets for reading subhalo and halo from the snapshots more efficiently
    :param base_path: The base path of the CAMELS simulation where the snapshot files are located
    :param offsets_path: The path where the calculated offsets will be saved
    :param snapshot: The snapshot for which the offsets will be calculated
    :return:
    """

    halos = il.groupcat.loadHalos(base_path, snapshot, fields=['GroupLenType', 'GroupNsubs'])
    halo_nsubs = halos['GroupNsubs']
    halo_offsets = halos['GroupLenType'].cumsum(axis=0)
    # Insert a zero-row in the beginning and remove last row
    halo_offsets = np.insert(halo_offsets, 0, 0, axis=0)[:-1, :]
    
    subhalos = il.groupcat.loadSubhalos(base_path, snapshot, fields=['SubhaloLenType'])
    subhalo_offsets = subhalos.cumsum(axis=0)
    # Insert a zero-row in the beginning and remove last row
    subhalo_offsets = np.insert(subhalo_offsets, 0, 0, axis=0)[:-1, :]
    
    # Fix offsets for the inner fuzz particles 
    halo_nsubs_cum = halo_nsubs.cumsum()
    subhalo_offsets_upd = np.copy(subhalo_offsets)
    sub_index = 0
    for hid in range(len(halo_nsubs) - 1):
        subhalos_halo = halo_nsubs[hid]
        subhalo_particles = np.sum(subhalos[sub_index:sub_index+subhalos_halo], axis=0)
        inner_fuzz = halo_offsets[hid+1] - halo_offsets[hid] - subhalo_particles
        sub_index += subhalos_halo
        
        # Update all subhalo offsets after the last subhalo of that halo
        subhalo_offsets_upd[halo_nsubs_cum[hid]:, ] += inner_fuzz
        
    offset_path = os.path.join(offsets_path, 'offsets_%03d.hdf5' % snapshot)
    with h5py.File(offset_path, 'w') as f:
        g_grp = f.create_group("Group")
        g_grp.create_dataset('SnapByType', data=halo_offsets)
        s_grp = f.create_group("Subhalo")
        s_grp.create_dataset('SnapByType', data=subhalo_offsets_upd)


def calc_offsets_sim(base_path, offsets_path, total_snapshots):
    """
    Calculate offsets for a specific simulation in parallel
    :param base_path: The base path of the simulation
    :param offsets_path: The path where the calculated offsets will be saved
    :param total_snapshots: The number of total snapshots of this simulation
    :return:
    """
    if not os.path.exists(offsets_path):
        os.makedirs(offsets_path)

    pool = Pool(processes=4)
    tqdm.tqdm(pool.starmap(create_offsets, zip(repeat(base_path),
                                               repeat(offsets_path),
                                               range(total_snapshots))),
              total=total_snapshots)
    pool.close()
    pool.join()


if __name__ == '__main__':

    suite_name_options = ('IllustrisTNG', 'Astrid', 'SIMBA')
    suite_name = input("Enter simulation suite for which you wish to do the offset calculation \n"
                       "(options: {}): ".format('/'.join(suite_name_options)))

    if suite_name not in suite_name_options:
        print('Suite outside of options!')
        sys.exit(1)

    sim_name = input("Enter simulation name: ")
    base_path = '/home/jovyan/PUBLIC_RELEASE/Sims/{}/{}/'.format(suite_name, sim_name)

    try:
        total_snapshots = len([name for name in os.listdir(base_path)
                               if os.path.isfile(os.path.join(base_path, name)) and name.startswith('snap_')])
    except OSError:
        print('Path {} does not seem to exist!'.format(base_path))
        sys.exit(1)

    offsets_path = os.path.join('/home/jovyan/home/Offsets/{}/{}'.format(suite_name, sim_name))
    save_path = input("Enter save path or leave blank for default ({}): ".format(offsets_path))
    if save_path:
        offsets_path = save_path

    if not os.path.exists(offsets_path):
        print('Calculating offsets for sim {}'.format(sim_name))
        calc_offsets_sim(base_path, offsets_path, total_snapshots)
    else:
        print('Offsets for sim {} already calculated!'.format(sim_name))
