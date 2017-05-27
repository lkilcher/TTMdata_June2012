from __future__ import print_function
# This script works with dolfyn version 0.3.6
import ttm.base as pmod
import matplotlib.pyplot as plt
import numpy as np
reload(pmod)
from collections import defaultdict
import matplotlib.dates as dt
from calendar import month_name as month
import ttm.June2012 as j12

flag = defaultdict(lambda: False, {})
flag['multi_spec01'] = True
#flag['time01'] = True
#flag['time_comb'] = True
#flag['save fig'] = True

tags = [
    'NREL',
    #'PNNL',
]

if 'data' not in vars():
    data = {}
print('')
for ftag in tags:
    print('Creating figures {}...'.format(ftag))
    if ftag not in data:
        print('  Loading data...')
        data[ftag] = j12.load(ftag, bin=True)

    dat = data[ftag]
    if flag['multi_spec01']:
        print('  Creating Spec01...', end=' ')
        fig, axs = pmod.multi_spec_plot(dat, 1100,
                                        uranges=np.arange(0, 2.6, 0.5),
                                        axsize=2,
                                        noise_level=dict(Spec=[1.6e-4, 1.6e-4, 5e-6],
                                                         Spec_uraw=[1.6e-4, 1.6e-4, 5e-6]))
        ax = axs[0, 0]
        ax.set_xlim([1e-3, 10])
        ax.set_ylim([1e-5, 1])
        figfile = 'fig/{}_Spec01.pdf'.format(ftag)
        print('saving ...', end='')
        if flag['save fig']:
            fig.savefig(figfile)
        print('Done.')

    if flag['time01']:
        print('  Creating Time01...', end=' ')
        fig, axs = pmod.vel_time(dat, 1200, )
        axs[0].set_ylim([-2.5, 2.5])
        axs[1].set_ylim([-1.0, 1.0])
        axs[2].yaxis.set_ticks(np.arange(-1, 1, 0.1))
        axs[2].set_ylim([-0.2, 0.2])
        axs[2].xaxis.set_major_locator(dt.HourLocator(range(0, 24, 6)))
        axs[2].xaxis.set_major_formatter(dt.DateFormatter('%d.%H'))
        axs[2].xaxis.set_minor_locator(dt.HourLocator())
        axs[2].set_xlabel('Local Time [Day.Hour {}, {}]'
                          .format(month[dat.mpltime.month[0] + 1], dat.mpltime.year[0]))
        figfile = 'fig/{}_VelTime01.pdf'.format(ftag)
        print('saving...', end=' ')
        if flag['save fig']:
            fig.savefig(figfile)
        print('Done.')

    if flag['time_comb']:
        print('  Creating VelComb01...', end=' ')
        fig, ax = pmod.vel_time_comb(dat, 1300, )
        ax.xaxis.set_major_locator(dt.HourLocator(range(0, 24, 6)))
        ax.xaxis.set_major_formatter(dt.DateFormatter('%d.%H'))
        ax.xaxis.set_minor_locator(dt.HourLocator())
        ax.set_xlabel('Local Time [Day.Hour {}, {}]'
                      .format(month[dat.mpltime.month[0] + 1], dat.mpltime.year[0]))
        figfile = 'fig/{}_VelComb01.pdf'.format(ftag)
        print('saving...', end=' ')
        if flag['save fig']:
            fig.savefig(figfile)
        print('Done.')
