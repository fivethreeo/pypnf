from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False

test_double_breakout_data = [
    5, 1, 6, 3, 7
]

test_double_breakdown_data = [
    3, 7, 2, 5, 1
]

def test_double_breakout():
    chart = PointFigureChart(
        {"close": test_double_breakout_data},
        "cl",
        3,
        1,
        "abs",
        "test_double_breakout"
    )
    if show_chart:
        chart.show()

    signals = {k:v.tolist() for k, v in chart.get_double_breakouts().items()}

    assert signals == {}

def test_double_breakdown():
    chart = PointFigureChart(
        {"close": test_double_breakdown_data},
        "cl",
        3,
        1,
        "abs",
        "test_double_breakdown"
    )
    if show_chart:
        chart.show()
    
    signals = {k:v.tolist() for k, v in chart.get_double_breakouts().items()}

    assert signals == {}