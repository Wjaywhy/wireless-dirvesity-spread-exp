"""Part 2 DSSS spread spectrum tests."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from part2_spread_spectrum import (  # type: ignore[import-not-found]
    dsss_despread,
    dsss_spread,
    generate_m_sequence,
    processing_gain_db,
)


def reference_m_sequence(register_state, taps, length=None):
    state = list(register_state)
    if length is None:
        length = 2 ** len(state) - 1
    output = []
    for _ in range(length):
        bit = state[-1]
        output.append(1 if bit == 0 else -1)
        feedback = 0
        for tap in taps:
            feedback ^= state[tap - 1]
        state = [feedback] + state[:-1]
    return np.array(output, dtype=int)


class TestSpreadSpectrum:
    def test_generate_m_sequence_matches_reference(self):
        sequence = generate_m_sequence([1, 1, 1], taps=[3, 2], length=7)
        expected = reference_m_sequence([1, 1, 1], taps=[3, 2], length=7)
        np.testing.assert_array_equal(sequence, expected)
        assert set(sequence.tolist()) <= {-1, 1}

    def test_generate_m_sequence_default_period(self):
        sequence = generate_m_sequence([1, 0, 0, 1], taps=[4, 1])
        assert len(sequence) == 15
        assert np.all(np.isin(sequence, [-1, 1]))

    def test_dsss_spread_expected_chips(self):
        bits = np.array([0, 1])
        pn = np.array([1, -1, 1, -1])
        expected = np.array([1, -1, 1, -1, -1, 1, -1, 1])
        np.testing.assert_array_equal(dsss_spread(bits, pn), expected)

    def test_dsss_despread_recovers_bits_with_small_noise(self):
        bits = np.array([0, 1, 1, 0, 0, 1])
        pn = np.array([1, -1, 1, -1, 1, -1, 1])
        chips = dsss_spread(bits, pn)
        noise = np.linspace(-0.2, 0.2, len(chips))
        recovered = dsss_despread(chips + noise, pn)
        np.testing.assert_array_equal(recovered, bits)

    def test_processing_gain(self):
        assert np.isclose(processing_gain_db(31), 10 * np.log10(31))

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            generate_m_sequence([0, 0, 0], taps=[1])
        with pytest.raises(ValueError):
            dsss_spread(np.array([0, 2]), np.array([1, -1]))
        with pytest.raises(ValueError):
            dsss_despread(np.ones(5), np.array([1, -1]))
        with pytest.raises(ValueError):
            processing_gain_db(0)


def test_dsss_result_files_exist():
    files = ['dsss_ber_curve.png', 'dsss_correlation_snapshot.png']
    missing = [name for name in files if not os.path.exists(os.path.join('results', name))]
    if missing:
        pytest.skip(f'尚未生成DSSS结果图: {missing}')
    for name in files:
        assert os.path.getsize(os.path.join('results', name)) > 1000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
