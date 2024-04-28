from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False

# closes
bullish_signal_reversed_data = [
    1, 6, 3, 7, 4, 8, 5, 9,4
]

bearish_signal_reversed_data = [
    10, 6, 9, 5, 8, 4, 7, 3, 8
]

# Bullish Signal Reversed
def test_bullish_signal_reversed():
    chart = PointFigureChart(
        {"close": bullish_signal_reversed_data},
        "cl",
        3,
        1,
        "abs",
        "test_bullish_signal_reversed"
    )
    if show_chart:
        chart.show()
    signals = chart.get_reversed_signals()

    assert signals == {
        'bottom box index': [
            2.0,
        ],
        'box index': [
            4,
        ],
        'column index': [
            7,
        ],
        'top box index': [
            9.0,
        ],
        'trend': [
            -1,
        ],
    }

# Bearish Signal Reversed
def test_bearish_signal_reversed():
    chart = PointFigureChart(
        {"close": bearish_signal_reversed_data},
        "cl",
        3,
        1,
        "abs",
        "test_bearish_signal_reversed"
    )
    if show_chart:
        chart.show()
    signals = chart.get_reversed_signals()

    assert signals == {
        'bottom box index': [
            7.0,
        ],
        'box index': [
            8,
        ],
        'column index': [
            7,
        ],
        'top box index': [
            9.0,
        ],
        'trend': [
            1,
        ],
    }
