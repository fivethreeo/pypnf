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
 
    signals = {k:v.tolist() for k, v in chart.get_asc_desc_triple_breakouts().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 3],
        'box index': [0, 0, 0, 0, 0, 8],
        'top box index': [0, 0, 0, 0, 0, 8],
        'ts index': [0, 0, 0, 0, 0, 6],
        'type': [0, 0, 0, 0, 0, 9],
        'width': [0, 0, 0, 0, 0, 5]
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
    
    signals = {k:v.tolist() for k, v in chart.get_asc_desc_triple_breakouts().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 3],
        'box index': [0, 0, 0, 0, 0, 1],
        'top box index': [0, 0, 0, 0, 0, 9],
        'ts index': [0, 0, 0, 0, 0, 6],
        'type': [0, 0, 0, 0, 0, 10],
        'width': [0, 0, 0, 0, 0, 5]
    }
