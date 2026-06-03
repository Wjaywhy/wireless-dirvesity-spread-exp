"""Run a small end-to-end performance smoke test after completing the TODOs."""

import numpy as np

from part1_diversity import simulate_diversity_ber
from part2_spread_spectrum import dsss_despread, dsss_spread, generate_m_sequence
from utils import calculate_ber, generate_bits


def main():
    print('=' * 60)
    print('分集与扩频通信实验 - 性能烟雾测试')
    print('=' * 60)

    curves = simulate_diversity_ber(np.array([6, 12]), num_bits=1000, num_branches=2, seed=7)
    print('分集 BER:', curves)

    bits = generate_bits(200, seed=8)
    pn = generate_m_sequence([1, 1, 1, 0, 1], taps=[5, 2], length=31)
    chips = dsss_spread(bits, pn)
    recovered = dsss_despread(chips, pn)
    print(f'DSSS 无噪声 BER: {calculate_ber(bits, recovered):.4g}')


if __name__ == '__main__':
    main()
