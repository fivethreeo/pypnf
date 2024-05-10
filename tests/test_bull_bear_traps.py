from pypnf import PointFigureChart
import os
# if SHOW_CHART var is in env set show_chart to True
if "SHOW_CHART" in os.environ:
    show_chart = True
else:
    show_chart = False

# closes
bull_trap_data = [
    1, 5, 2, 5, 2, 6, 3
]

bear_trap_data = [
    3, 10, 9, 3, 8, 3, 6, 5, 2, 5
]

# Bull Trap
def test_bull_trap():
    chart = PointFigureChart(
        {"close": bull_trap_data},
        "cl",
        3,
        1,
        "abs",
        "test_bull_trap"
    )
    if show_chart:
        chart.show()
   
    signals = {k:v.tolist() for k, v in chart.get_traps().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 2],
        'box index': [0, 0, 0, 0, 0, 4],
        'top box index': [0, 0, 0, 0, 0, 7],
        'ts index': [0, 0, 0, 0, 0, 6],
        'type': [0, 0, 0, 0, 0, 18],
        'width': [0, 0, 0, 0, 0, 6]
    }

# Bear Trap
def test_bear_trap():
    chart = PointFigureChart(
        {"close": bear_trap_data},
        "cl",
        3,
        1,
        "abs",
        "test_bear_trap"
    )

    if show_chart:
        chart.show()
    
    signals = {k:v.tolist() for k, v in chart.get_traps().items()}

    assert signals == {
        'bottom box index': [0, 0, 0, 0, 0, 0, 3],
        'box index': [0, 0, 0, 0, 0, 0, 6],
        'top box index': [0, 0, 0, 0, 0, 0, 10],
        'ts index': [0, 0, 0, 0, 0, 0, 0],
        'type': [0, 0, 0, 0, 0, 0, 19],
        'width': [0, 0, 0, 0, 0, 0, 6]
    }
