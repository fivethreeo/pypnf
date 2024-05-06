from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False

test_triple_breakout_data = [   
    6, 1, 7, 3, 7, 4, 8
]

test_triple_breakdown_data = [
    3, 8, 2, 6, 2, 5, 1
]

def test_triple_breakout():
    chart = PointFigureChart(
        {"close": test_triple_breakout_data},
        "cl",
        3,
        1,
        "abs",
        "test_triple_breakout"
    )
    if show_chart:
        chart.show()
 
    signals = {k:v.tolist() for k, v in chart.get_triple_breakouts().items()}

    assert signals == {}

def test_triple_breakdown():
    chart = PointFigureChart(
        {"close": test_triple_breakdown_data},
        "cl",
        3,
        1,
        "abs",
        "test_triple_breakdown"
    )
    if show_chart:
        chart.show()
    
    signals = {k:v.tolist() for k, v in chart.get_triple_breakouts().items()}

    assert signals == {}