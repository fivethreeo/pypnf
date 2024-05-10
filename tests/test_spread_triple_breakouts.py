from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False


test_spread_triple_breakout_data = [
    1, 8, 2, 8, 3, 7, 4, 9
]

test_spread_triple_breakdown_data = [
    9, 2, 8, 2, 6, 3, 6, 1
]

def test_spread_triple_breakout():
    chart = PointFigureChart(
        {"close": test_spread_triple_breakout_data},
        "cl",
        3,
        1,
        "abs",
        "test_spread_triple_breakout"
    )
    if show_chart:
        chart.show()
 
    signals = {k:v.tolist() for k, v in chart.get_spread_triple_breakouts().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 0, 2],
        'box index': [0, 0, 0, 0, 0, 0, 9],
        'top box index': [0, 0, 0, 0, 0, 0, 10],
        'ts index': [0, 0, 0, 0, 0, 0, 7],
        'type': [0, 0, 0, 0, 0, 0, 19],
        'width': [0, 0, 0, 0, 0, 0, 7]
    }


def test_spread_triple_breakdown():
    chart = PointFigureChart(
        {"close": test_spread_triple_breakdown_data},
        "cl",
        3,
        1,
        "abs",
        "test_spread_triple_breakdown"
    )
    if show_chart:
        chart.show()
    
    signals = {k:v.tolist() for k, v in chart.get_spread_triple_breakouts().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 0, 2],
        'box index': [0, 0, 0, 0, 0, 0, 1],
        'top box index': [0, 0, 0, 0, 0, 0, 10],
        'ts index': [0, 0, 0, 0, 0, 0, 7],
        'type': [0, 0, 0, 0, 0, 0, 20],
        'width': [0, 0, 0, 0, 0, 0, 7]
    }
