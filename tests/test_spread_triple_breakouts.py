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

    assert signals == {}

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

    assert signals == {}