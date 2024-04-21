from pypnf import PointFigureChart

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
    # chart.show()
    triangles = chart.get_triangles()

    assert triangles == {
        'box index': [9],
        'column index': [6],
        'height': [11.0],
        'trend': [1],
        'width': [5]
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
    # chart.show()
    triangles = chart.get_triangles()

    assert triangles == {
        'box index': [3],
        'column index': [7],
        'height': [11.0],
        'trend': [-1],
        'width': [6]
    }