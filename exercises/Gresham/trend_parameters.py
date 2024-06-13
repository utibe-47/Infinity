from collections import OrderedDict

from momentum_strategy_signals import (calculate_bollinger_band_signal, calculate_moving_average,
                                       calculate_breakout_signal)


dict_rf_fx_trend = {
    'bollinger_band': {
        'function': calculate_bollinger_band_signal,
        'list_params': [
            OrderedDict([('window_long', 250), ('window_short', 1), ('std_factor', 1.), ('allocation', .12)]),
            OrderedDict([('window_long', 200), ('window_short', 1), ('std_factor', 1.5), ('allocation', .12)]),
            OrderedDict([('window_long', 160), ('window_short', 1), ('std_factor', 1.2), ('allocation', .03)]),
            OrderedDict([('window_long', 120), ('window_short', 1), ('std_factor', 1.0), ('allocation', .03)]),
            OrderedDict([('window_long', 100), ('window_short', 1), ('std_factor', 1.0), ('allocation', .03)]),
            OrderedDict([('window_long', 80), ('window_short', 1), ('std_factor', 1.5), ('allocation', .03)])
        ]
    },

    'simple_moving_average': {
        'function': calculate_moving_average,
        'list_params': [
            OrderedDict([('window_long', 252), ('window_short', 8), ('allocation', .12)]),
            OrderedDict([('window_long', 252), ('window_short', 20), ('allocation', .12)]),
            OrderedDict([('window_long', 160), ('window_short', 10), ('allocation', .03)]),
            OrderedDict([('window_long', 120), ('window_short', 10), ('allocation', .03)]),
            OrderedDict([('window_long', 80), ('window_short', 5), ('allocation', .03)]),
            OrderedDict([('window_long', 60), ('window_short', 2), ('allocation', .03)])
        ]
    },

    'breakout': {
        'function': calculate_breakout_signal,
        'list_params': [
            OrderedDict([('window', 200), ('min_periods', 10), ('allocation', .12)]),
            OrderedDict([('window', 180), ('min_periods', 10), ('allocation', .12)]),
            OrderedDict([('window', 140), ('min_periods', 10), ('allocation', .03)]),
            OrderedDict([('window', 120), ('min_periods', 10), ('allocation', .03)]),
            OrderedDict([('window', 90), ('min_periods', 10), ('allocation', .03)]),
            OrderedDict([('window', 60), ('min_periods', 10), ('allocation', .03)])
        ]
    },
}
