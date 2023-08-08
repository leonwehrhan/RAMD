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


def residence_time_distribution(ax, bs_res_times, n_bins=6, **kwargs):
    '''
    Plot histogram of bootstrapped effective residence times and a normal distribution based on the data.

    Parameters
    ----------
    ax : plt.Axes
        Matplotlib plot.
    bs_res_times : np.ndarray
        Bootstrapped effective residence times.
    n_bins : int
        Number of bins for histogram.
    '''
    # plot histogram
    ax.hist(bs_res_times, bins=n_bins, density=True, alpha=0.4, color='k')

    # calculate mean and std parameters of normal distribution
    loc, scale = stats.norm.fit(bs_res_times)

    # plot normal distribution
    xmin, xmax = plt.xlim()
    xs = np.linspace(0.8 * xmin, xmax, 100)
    ys = stats.norm.pdf(xs, loc, scale)
    ax.plot(xs, ys, **kwargs)
    ax.text(0.02, 0.98, f'Eff. Res. Time: {round(loc, 3)} +/- {round(scale, 3)} ns', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

    ax.set_xlabel('Effective Residence Time [ns]')
    ax.set_ylabel('Probability Density')