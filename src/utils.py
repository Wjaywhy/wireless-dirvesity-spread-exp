"""Common utilities for the diversity and spread spectrum experiment."""

import os

import matplotlib.pyplot as plt
import numpy as np


def setup_chinese_font():
    """Configure Matplotlib fonts for Chinese labels."""
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False


def ensure_results_dir():
    """Ensure the results directory exists."""
    os.makedirs('results', exist_ok=True)


def generate_bits(num_bits, seed=None):
    """Generate random 0/1 bits."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, int(num_bits), dtype=int)


def bpsk_modulate(bits):
    """BPSK mapping: 0 -> +1, 1 -> -1."""
    bits = np.asarray(bits, dtype=int)
    return 1.0 - 2.0 * bits


def bpsk_demodulate(symbols):
    """BPSK hard decision."""
    return (np.real(symbols) < 0).astype(int)


def calculate_ber(bits_tx, bits_rx):
    """Calculate bit error rate."""
    bits_tx = np.asarray(bits_tx, dtype=int)
    bits_rx = np.asarray(bits_rx, dtype=int)
    length = min(len(bits_tx), len(bits_rx))
    if length == 0:
        raise ValueError('bit sequences must not be empty')
    return float(np.mean(bits_tx[:length] != bits_rx[:length]))


def add_awgn(signal, snr_db, seed=None):
    """Add AWGN to a real or complex signal using measured signal power."""
    rng = np.random.default_rng(seed)
    signal = np.asarray(signal)
    power = np.mean(np.abs(signal) ** 2)
    noise_power = power / (10 ** (snr_db / 10))
    if np.iscomplexobj(signal):
        noise = (rng.normal(0, np.sqrt(noise_power / 2), signal.shape)
                 + 1j * rng.normal(0, np.sqrt(noise_power / 2), signal.shape))
    else:
        noise = rng.normal(0, np.sqrt(noise_power), signal.shape)
    return signal + noise


def rayleigh_fading_branches(symbols, num_branches, snr_db, seed=None):
    """Simulate independent flat Rayleigh fading branches."""
    if num_branches <= 0:
        raise ValueError('num_branches must be positive')
    rng = np.random.default_rng(seed)
    symbols = np.asarray(symbols, dtype=float)
    shape = (int(num_branches), len(symbols))
    channel = (rng.normal(0, 1 / np.sqrt(2), shape)
               + 1j * rng.normal(0, 1 / np.sqrt(2), shape))
    faded = channel * symbols[np.newaxis, :]
    signal_power = np.mean(np.abs(faded) ** 2)
    noise_power = signal_power / (10 ** (snr_db / 10))
    noise = (rng.normal(0, np.sqrt(noise_power / 2), shape)
             + 1j * rng.normal(0, np.sqrt(noise_power / 2), shape))
    return faded + noise, channel


def add_narrowband_interference(signal, amplitude=0.8, frequency=0.03, phase=0.0):
    """Add a sinusoidal narrowband interferer to a chip sequence."""
    signal = np.asarray(signal, dtype=float)
    index = np.arange(len(signal))
    interference = amplitude * np.cos(2 * np.pi * frequency * index + phase)
    return signal + interference


def plot_ber_curve(x_values, curves, title, filename):
    """Plot BER curves."""
    setup_chinese_font()
    ensure_results_dir()
    plt.figure(figsize=(8, 5))
    for label, values in curves.items():
        plt.semilogy(x_values, np.maximum(values, 1e-5), marker='o', linewidth=2, label=label)
    plt.xlabel('SNR (dB)')
    plt.ylabel('BER')
    plt.title(title)
    plt.grid(True, which='both', alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename), dpi=300)
    plt.close()


def plot_diversity_snapshot(symbols, branch_output, mrc_output, filename):
    """Plot a short waveform snapshot before and after MRC."""
    setup_chinese_font()
    ensure_results_dir()
    length = min(80, len(symbols), len(branch_output), len(mrc_output))
    plt.figure(figsize=(10, 5))
    plt.plot(symbols[:length], label='发送BPSK符号', linewidth=1.5)
    plt.plot(np.real(branch_output[:length]), label='单分支均衡输出', alpha=0.75)
    plt.plot(np.real(mrc_output[:length]), label='MRC合并输出', alpha=0.85)
    plt.xlabel('符号序号')
    plt.ylabel('幅度')
    plt.title('分集合并前后波形快照')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename), dpi=300)
    plt.close()


def plot_correlation_snapshot(correlations, filename):
    """Plot DSSS per-symbol correlation outputs."""
    setup_chinese_font()
    ensure_results_dir()
    correlations = np.asarray(correlations, dtype=float)
    length = min(80, len(correlations))
    plt.figure(figsize=(10, 4.8))
    markerline, stemlines, baseline = plt.stem(np.arange(length), correlations[:length])
    markerline.set_markersize(3)
    stemlines.set_linewidth(1.0)
    baseline.set_linewidth(0.8)
    plt.axhline(0, color='black', linewidth=1)
    plt.xlabel('符号序号')
    plt.ylabel('相关输出')
    plt.title('DSSS解扩相关输出快照')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join('results', filename), dpi=300)
    plt.close()
