import pytest
import numpy as np
import matplotlib.pyplot as plt
import os
from context import tRAMD
from context import plot



@pytest.fixture
def times_results():
    
    times = [1.742, 2.477, 3.308, 3.743, 4.432, 6.199, 6.374, 7.953, 9.337, 10.099, 10.374, 10.403, 12.55, 18.382, 19.517]
    return times


def test_read_dissociation_times(times_results):
    times_ref = times_results
    times = tRAMD.read_dissociation_times('test_data.out', mode='out', timestep=2e-6)
    assert np.allclose(times_ref, times, atol=1e-3)


def test_bootstrap_residence_times():
    
    times = tRAMD.read_dissociation_times('test_data.out', mode='out', timestep=2e-6)
    bs_res_times = tRAMD.bootstrap_residence_times(times, n_samples=50000, sample_size=None)

    assert len(bs_res_times) == 50000


def test_plots():

    times = tRAMD.read_dissociation_times('test_data.out', mode='out', timestep=2e-6)
    bs_res_times = tRAMD.bootstrap_residence_times(times, n_samples=50000, sample_size=None)

    fig, ax = plt.subplots()
    plot.cumulative_histogram(ax, times)
    plt.savefig('test_hist.png', dpi=75)
    plt.close()

    fig, ax = plt.subplots()
    plot.residence_time_distribution(ax, bs_res_times, n_bins=6)
    plt.savefig('test_t_eff.png', dpi=75)
    plt.close()

    assert os.path.exists('test_hist.png')
    assert os.path.exists('test_t_eff.png')

    os.remove('test_hist.png')
    os.remove('test_t_eff.png')