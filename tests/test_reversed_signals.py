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

    signals = {k:v.tolist() for k, v in chart.get_reversed_signals().items()}

    assert signals == {
        'bottom box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0],
        'box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0],
        'top box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0],
        'type': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 14.0],
        'width': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0]
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

    signals = {k:v.tolist() for k, v in chart.get_reversed_signals().items()}

    assert signals == {
        'bottom box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0],
        'box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.0],
        'top box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0],
        'type': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 13.0],
        'width': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0]
    }
