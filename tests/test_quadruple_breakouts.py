from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False


test_quadruple_breakout_data = [
    6, 1, 7, 2, 7, 3, 7, 4, 8
]

test_quadruple_breakdown_data = [
    3, 8, 2, 7, 2, 6, 2, 5, 1
]

def test_quadruple_breakout():
    chart = PointFigureChart(
        {"close": test_quadruple_breakout_data},
        "cl",
        3,
        1,
        "abs",
        "test_quadruple_breakout"
    )
    if show_chart:
        chart.show()
 
    signals = {k:v.tolist() for k, v in chart.get_quadruple_breakouts().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 0, 0, 2],
        'box index': [0, 0, 0, 0, 0, 0, 0, 8],
        'top box index': [0, 0, 0, 0, 0, 0, 0, 9],
        'ts index': [0, 0, 0, 0, 0, 0, 0, 8],
        'type': [0, 0, 0, 0, 0, 0, 0, 6],
        'width': [0, 0, 0, 0, 0, 0, 0, 7]
    }

    
def test_quadruple_breakdown():
    chart = PointFigureChart(
        {"close": test_quadruple_breakdown_data},
        "cl",
        3,
        1,
        "abs",
        "test_quadruple_breakdown"
    )
    if show_chart:
        chart.show()
    
    signals = {k:v.tolist() for k, v in chart.get_quadruple_breakouts().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 0, 0, 2],
        'box index': [0, 0, 0, 0, 0, 0, 0, 1],
        'top box index': [0, 0, 0, 0, 0, 0, 0, 9],
        'ts index': [0, 0, 0, 0, 0, 0, 0, 8],
        'type': [0, 0, 0, 0, 0, 0, 0, 7],
        'width': [0, 0, 0, 0, 0, 0, 0, 7]
    }
