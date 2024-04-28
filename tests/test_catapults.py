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
    catapults = chart.get_catapults()

    assert catapults == {
        'bottom box index': [
            2.0,
        ],
        'box index': [
            7,
        ],
        'column index': [
            7,
        ],
        'top box index': [
            7.0,
        ],
        'trend': [
            1,
        ],
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
    catapults = chart.get_catapults()

    assert catapults == {
        'bottom box index': [
            3.0,
        ],
        'box index': [
            1,
        ],
        'column index': [
            7,
        ],
        'top box index': [
            7.0,
        ],
        'trend': [
            -1,
        ],
    }
