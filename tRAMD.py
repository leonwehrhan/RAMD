import numpy as np
import re
import plot


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
        if isinstance(files, str):
            fi = files
        elif isinstance(files, list):
            fi = files[0]

        with open(fi, 'r') as f:
            for line in f.readlines():
                if re.match(r'==== RAMD ==== GROMACS will be stopped', line):
                    s = re.search(r'[0-9]+', line)[0]
                    t = int(s) * timestep
                    times.append(t)

    else:
        raise ValueError('mode must be "log" or "out".')

    if isinstance(files, list):
        print(f'Found {len(times)} dissociation times in {len(files)} files.')
    else:
        print(f'Found {len(times)} dissociation times in 1 file.')

    times = np.array(times)
    times = np.sort(times)

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
    if not sample_size:
        sample_size = int(0.8 * len(times))
    
    bs_res_times = []

    print(f'Calculating {n_samples} bootstrap samples with a size of {sample_size} from {len(times)} dissociation times.')
    print(f'Median of dissociation times: {round(np.median(times), 3)}')

    for i in range(n_samples):
        # shuffle dissociation times and select bootstrap sample group
        np.random.shuffle(times)
        sample = times[:sample_size]
        sample = np.sort(sample)

        # calculate efective residence time
        eff_rs = np.median(sample)
        bs_res_times.append(eff_rs)
    
    return np.array(bs_res_times)


def main():
    pass


if __name__ == '__main__':
    main()