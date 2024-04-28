from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False


asc_desc_triple_breakout_data = [
    5, 1, 6, 3, 7, 4, 8
]

asc_desc_triple_breakdown_data = [
    5, 9, 4, 7, 2, 5, 1
]


def test_asc_desc_triple_breakout():
    chart = PointFigureChart(
        {"close": asc_desc_triple_breakout_data},
        "cl",
        3,
        1,
        "abs",
        "test_asc_desc_triple_breakout"
    )
    if show_chart:
        chart.show()
    asc_desc_triple_breakouts = chart.get_asc_desc_triple_breakouts()

    assert asc_desc_triple_breakouts == {
        'bottom box index': [
            3.0,
        ],
        'box index': [
            8,
        ],
        'column index': [
            5,
        ],
        'top box index': [
            8.0,
        ],
        'trend': [
            1,
        ],
    }

def test_asc_desc_triple_breakdown():
    chart = PointFigureChart(
        {"close": asc_desc_triple_breakdown_data},
        "cl",
        3,
        1,
        "abs",
        "test_bearish_triangle_breakdown"
    )
    if show_chart:
        chart.show()
    asc_desc_triple_breakouts = chart.get_asc_desc_triple_breakouts()

    assert asc_desc_triple_breakouts == {
        'bottom box index': [
            3.0,
        ],
        'box index': [
            1,
        ],
        'column index': [
            5,
        ],
        'top box index': [
            9.0,
        ],
        'trend': [
            -1,
        ],
    }
