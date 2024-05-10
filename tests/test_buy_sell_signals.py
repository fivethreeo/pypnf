from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False

test_buy_signal_data = [
    8, 1 , 5, 2, 7, 2
]

test_sell_signal_data = [
    1, 7, 2, 5, 1, 5
]
    

def test_buy_signal():
    chart = PointFigureChart(
        {"close": test_buy_signal_data},
        "cl",
        3,
        1,
        "abs",
        "test_buy_signal"
    )
    if show_chart:
        chart.show()

    signals = {k:v.tolist() for k, v in chart.get_buy_sell_signals().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 3, 0],
        'box index': [0, 0, 0, 8, 0],
        'top box index': [0, 0, 0, 8, 0],
        'ts index': [0, 0, 0, 0, 0],
        'type': [0, 0, 0, 0, 0],
        'width': [0, 0, 0, 3, 0]
    }

def test_sell_signal():
    chart = PointFigureChart(
        {"close": test_sell_signal_data},
        "cl",
        3,
        1,
        "abs",
        "test_sell_signal"
    )
    if show_chart:
        chart.show()

    signals = {k:v.tolist() for k, v in chart.get_buy_sell_signals().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 2, 0],
        'box index': [0, 0, 0, 2, 0],
        'top box index': [0, 0, 0, 6, 0],
        'ts index': [0, 0, 0, 4, 0],
        'type': [0, 0, 0, 1, 0],
        'width': [0, 0, 0, 3, 0]
    }