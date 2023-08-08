import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def cumulative_histogram(ax, times, **kwargs):
    '''
    Plot cumulative histogram of dissociation times.

    Parameters
    ----------
    ax : plt.Axes
        Matplotlib plot.
    times : np.ndarray
        Dissociation times for one replica.
    '''
    numbins = int(len(times) / 2)
    chist = stats.cumfreq(times, numbins=numbins)

    xs = chist.lowerlimit + np.linspace(0, chist.binsize * chist.cumcount.size, chist.cumcount.size)
    ys = chist.cumcount

    ax.step(xs, ys, where='mid', **kwargs)

    ax.set_xlabel('Dissociation Time [ns]')
    ax.set_ylabel('N_trj')