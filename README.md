# README #

Custom version to work with the CAMELS project data.

The Illustris Simulation: Public Data Release

Example code (Python).


See the [Illustris Website Data Access Page](http://www.illustris-project.org/data/) for details.

See the [CAMELS docs](https://camels.readthedocs.io/en/latest/) for details.


# Install


```
git clone git@github.com:eagel27/illustris_python_CAMELS.git
cd illustris_python
pip install .
```
# Prerequisites

The snapshot offsets need to be calculated prior to using this package. 
This can be done with the python script create_snapshot_offsets.py (follow instructions on prompt):

```
python create_snapshot_offsets.py
```

# Usage

The usage is similar to the illustris_python package. 

!! Important !! \
To load subhalos and halos from the snapshot files, the snapshot offsets 
should be calculated (see prerequisites) and the path should be provided in the arguments:



```
import illustris_python_CAMELS.illustris_python as il

il.snapshot.loadSubhalo('/home/jovyan/Data/Sims/IllustrisTNG/1P/1P_1_0',
                         33, 0, 'stars', 
                         fields=['ParticleIDs', 'GFM_StellarFormationTime', 'Masses'], 
                         overwrite_path='/home/jovyan/home/snapshot_offsets/')
```
