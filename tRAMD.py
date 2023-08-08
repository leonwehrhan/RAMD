import numpy as np
import re


def read_dissociation_times(files, mode='log', timestep=2e-6):
    '''
    Read either .log files or .out file to gather the dissociation times from RAMD simulations

    Parameters
    ----------
    files : str or list
        Paths to .log/.out files. Must be list for .log, can be str or list with length 1 for .out.
    mode : str
        Whether to read .log or .out files. Either "log" or "out".
    timestep : float
        Simulation timestep in ns.
    
    Returns
    -------
    times : np.ndarray
        Dissociation times in ns.
    '''
    times = []

    if mode == 'log':
        for fi in files:
            with open(fi, 'r') as f:
                for line in f.readlines():
                    if re.match(r'==== RAMD ==== GROMACS will be stopped', line):
                        s = re.search(r'[0-9]+', line)[0]
                        t = round(int(s) * timestep, 3)
                        times.append(t)
    
    elif mode == 'out':
        if files.isinstance(str):
            fi = files
        elif files.isinstance(list):
            fi = files[0]
            with open(fi, 'r') as f:
                for line in f.readlines():
                    if re.match(r'==== RAMD ==== GROMACS will be stopped', line):
                        s = re.search(r'[0-9]+', line)[0]
                        t = int(s) * timestep
                        times.append(t)

    else:
        raise ValueError('mode must be "log" or "out".')

    if files.isinstance(list):
        print(f'Found {len(times)} dissociation times in {len(files)} files.')
    else:
        print(f'Found {len(times)} dissociation times in 1 file.')

    return times


def bootstrap_residence_times(times, n_samples=50000, sample_size=None):
    '''
    Bootstrap dissociation times and calculate effective residence (after 50% of trjs have dissociated) times from samples.

    Parameters
    ----------
    times : np.ndarray
        Dissociation times in ns.
    n_samples : int
        Number of bootstrap sample groups.
    sample_size : int or None
        Size of sample groups.
    
    Returns
    -------
    bs_res_times : np.ndarray
        Bootstrapped effective residence times.
    '''