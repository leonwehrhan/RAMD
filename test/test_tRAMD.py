import pytest
import numpy as np
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