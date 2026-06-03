"""Generate example outputs after students complete the TODO functions."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from part1_diversity import run_diversity_demo  # type: ignore[import-not-found]
from part2_spread_spectrum import run_spread_spectrum_demo  # type: ignore[import-not-found]


def main():
    print('Generating Experiment 03 example outputs...')
    run_diversity_demo()
    run_spread_spectrum_demo()


if __name__ == '__main__':
    main()
