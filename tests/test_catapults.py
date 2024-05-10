from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False


bullish_catapult_data = [
   4, 2, 1, 5, 2, 1, 5, 2, 6, 3, 7
]

bearish_catapult_data = [
    4, 6, 3, 6, 3, 6, 2, 5, 1
]

def test_bullish_catapult():
    chart = PointFigureChart(
        {"close": bullish_catapult_data},
        "cl",
        3,
        1,
        "abs",
        "test_bullish_catapult"
    )
    if show_chart:
        chart.show()
  
    signals = {k:v.tolist() for k, v in chart.get_catapults().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 0, 0, 2],
        'box index': [0, 0, 0, 0, 0, 0, 0, 7],
        'top box index': [0, 0, 0, 0, 0, 0, 0, 7],
        'ts index': [0, 0, 0, 0, 0, 0, 0, 10],
        'type': [0, 0, 0, 0, 0, 0, 0, 11],
        'width': [0, 0, 0, 0, 0, 0, 0, 7]
    }

def test_bearish_catapult():
    chart = PointFigureChart(
        {"close": bearish_catapult_data},
        "cl",
        3,
        1,
        "abs",
        "test_bearish_catapult"
    )
    if show_chart:
        chart.show()
    
    signals = {k:v.tolist() for k, v in chart.get_catapults().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 0, 0, 3],
        'box index': [0, 0, 0, 0, 0, 0, 0, 1],
        'top box index': [0, 0, 0, 0, 0, 0, 0, 7],
        'ts index': [0, 0, 0, 0, 0, 0, 0, 8],
        'type': [0, 0, 0, 0, 0, 0, 0, 12],
        'width': [0, 0, 0, 0, 0, 0, 0, 7]
    }