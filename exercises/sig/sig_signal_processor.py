import numpy as np
from matplotlib import pyplot as plt
from scipy import fftpack
from statsmodels.tsa.seasonal import seasonal_decompose
from arch.unitroot import *


def fft_implementation(data):
    # Frequency and sampling rate
    sample_rate = data.shape[0]  # sampling rate
    t = np.arange(0, 1, 1/sample_rate)  # Sine function
    y = data.values  # Perform Fourier transform using scipy

    y_fft = fftpack.fft(data.values)  # Plot data
    n = data.shape[0]
    fr = sample_rate/2 * np.linspace(0, 1, int(np.floor(n/2)))
    y_m = 2/n * abs(y_fft[0:np.size(fr)])
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    ax[0].plot(t, y)    # plot time series
    ax[1].stem(fr, y_m)  # plot freq domain
    plt.show()


def decompose_signal(data):
    result = seasonal_decompose(data, period=1)
    plt.rcParams.update({'font.size': 14})
    fig = result.plot()
    fig.set_size_inches((16, 9))
    fig.tight_layout()
    plt.savefig('signal_decomposition' + '.png')
    plt.show()


def unit_root_test(data):
    aug_dickey_fuller_ct = ADF(data, trend='ct')
    print(aug_dickey_fuller_ct.summary())

    aug_dickey_fuller_c = ADF(data, trend='c')
    print(aug_dickey_fuller_c.summary())

    aug_dickey_fuller_n = ADF(data, trend='n')
    print(aug_dickey_fuller_n.summary())

    kpss_ct = KPSS(data, trend='ct')
    print(kpss_ct.summary())

    php_ct = PhillipsPerron(data, trend='ct')
    print(php_ct.summary())

