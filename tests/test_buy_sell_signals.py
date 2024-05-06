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

    assert signals == {}

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

    assert signals == {}