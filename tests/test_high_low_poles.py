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
    
    signals = {k:v.tolist() for k, v in chart.get_high_low_poles().items()}

    assert chart.ts['close'][signals['ts index'][3]] == 5

    assert signals == {
        'bottom box index': [0, 0, 0, 3],
        'box index': [0, 0, 0, 6],
        'top box index': [0, 0, 0, 11],
        'ts index': [0, 0, 0, 4],
        'type': [0, 0, 0, 22],
        'width': [0, 0, 0, 3]
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
    signals = {k:v.tolist() for k, v in chart.get_high_low_poles().items()}

    assert chart.ts['close'][signals['ts index'][3]] == 6

    assert signals == {
        'bottom box index': [0, 0, 0, 3],
        'box index': [0, 0, 0, 6],
        'top box index': [0, 0, 0, 11],
        'ts index': [0, 0, 0, 4],
        'type': [0, 0, 0, 23],
        'width': [0, 0, 0, 3]
    }
