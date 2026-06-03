"""Part 1 diversity combining tests."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import pytest
from part1_diversity import maximal_ratio_combining, selection_combining, simulate_diversity_ber  # type: ignore[import-not-found]


class TestDiversityCombining:
    def test_selection_combining_chooses_strongest_branch(self):
        symbols = np.array([1.0, -1.0, 1.0])
        channel = np.array([
            [0.2 + 0j, 1.0 + 0j, 0.3 + 0j],
            [1.0 + 0j, 0.1 + 0j, 2.0 + 0j],
        ])
        received = channel * symbols[np.newaxis, :]
        combined = selection_combining(received, channel)
        np.testing.assert_allclose(combined, symbols, atol=1e-10)

    def test_mrc_recovers_symbols_without_noise(self):
        symbols = np.array([1.0, -1.0, 1.0, -1.0])
        channel = np.array([
            [0.4 + 0.1j, 0.8 - 0.3j, 0.2 + 0.5j, 0.7 + 0.2j],
            [1.1 - 0.2j, 0.3 + 0.4j, 0.9 - 0.1j, 0.6 - 0.6j],
        ])
        received = channel * symbols[np.newaxis, :]
        combined = maximal_ratio_combining(received, channel)
        np.testing.assert_allclose(combined, symbols, atol=1e-10)

    def test_mrc_matches_formula(self):
        received = np.array([[1 + 1j, -1 + 0.2j], [0.4 - 0.5j, -0.8 + 0.1j]])
        channel = np.array([[0.8 + 0.2j, 0.6 - 0.1j], [0.3 - 0.4j, 0.5 + 0.2j]])
        expected = np.sum(np.conj(channel) * received, axis=0) / np.sum(np.abs(channel) ** 2, axis=0)
        np.testing.assert_allclose(maximal_ratio_combining(received, channel), expected)

    def test_simulate_diversity_ber_shape_and_range(self):
        curves = simulate_diversity_ber(np.array([0, 6]), num_bits=800, num_branches=2, seed=42)
        assert set(curves) == {'单分支', 'SC', 'MRC'}
        for values in curves.values():
            assert len(values) == 2
            assert np.all(np.isfinite(values))
            assert np.all((np.asarray(values) >= 0) & (np.asarray(values) <= 1))

    def test_mrc_improves_high_snr_over_single_branch(self):
        curves = simulate_diversity_ber(np.array([10]), num_bits=3000, num_branches=2, seed=99)
        assert curves['MRC'][0] <= curves['单分支'][0]

    def test_invalid_inputs(self):
        with pytest.raises(ValueError):
            selection_combining(np.array([1, 2]), np.array([1, 2]))
        with pytest.raises(ValueError):
            maximal_ratio_combining(np.ones((2, 2)), np.ones((2, 3)))
        with pytest.raises(ValueError):
            simulate_diversity_ber([], num_bits=100, num_branches=2)


def test_diversity_result_files_exist():
    files = ['diversity_ber_curve.png', 'diversity_waveform_snapshot.png']
    missing = [name for name in files if not os.path.exists(os.path.join('results', name))]
    if missing:
        pytest.skip(f'尚未生成分集结果图: {missing}')
    for name in files:
        assert os.path.getsize(os.path.join('results', name)) > 1000


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
