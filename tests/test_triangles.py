from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False

bullish_triangle_breakout_data = [
    1, 11, 2, 9, 4, 8, 5, 9
]

bearish_triangle_breakdown_data = [
    1, 11, 2, 9, 3, 8, 4, 7, 3
]


def test_bullish_triangle_breakout():
    chart = PointFigureChart(
        {"close": bullish_triangle_breakout_data},
        "cl",
        3,
        1,
        "abs",
        "test_bullish_triangle_breakout"
    )
    if show_chart:
        chart.show()

    triangles = {k:v.tolist() for k, v in chart.get_triangles().items()}

    assert triangles == {
        'bottom box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0],
        'box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0],
        'top box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 11.0],
        'type': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 14.0],
        'width': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0]
    }


def test_bearish_triangle_breakdown():
    chart = PointFigureChart(
        {"close": bearish_triangle_breakdown_data},
        "cl",
        3,
        1,
        "abs",
        "test_bearish_triangle_breakdown"
    )
    if show_chart:
        chart.show()
        
    triangles = {k:v.tolist() for k, v in chart.get_triangles().items()}

    assert triangles == {
        'bottom box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0],
        'box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0],
        'top box index': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 11.0],
        'type': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 15.0],
        'width': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0]
    }
