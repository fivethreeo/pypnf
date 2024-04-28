from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False

high_pole_data = [
    1, 6, 2, 10, 5
]

low_pole_data = [
    12, 6, 10, 2, 6
]

# High Pole
def test_high_pole():
    chart = PointFigureChart(
        {"close": high_pole_data},
        "cl",
        3,
        1,
        "abs",
        "test_high_pole"
    )
    if show_chart:
        chart.show()
    poles = chart.get_high_low_poles()

    assert poles == {
        'bottom box index': 3.0,
        'box index': [
            6.0,
        ],
        'column index': [
            3,
        ],
        'top box index': 11.0,
        'trend': [
            -1.0,
        ],
    }

# Low Pole
def test_low_pole():
    chart = PointFigureChart(
        {"close": low_pole_data},
        "cl",
        3,
        1,
        "abs",
        "test_low_pole"
    )
    if show_chart:
        chart.show()
    poles = chart.get_high_low_poles()

    assert poles == {
        'bottom box index': 3.0,
        'box index': [
            7.0,
        ],
        'column index': [
            3,
        ],
        'top box index': 11.0,
        'trend': [
            1.0,
        ],
    }
