from pypnf import PointFigureChart

# closes
bull_trap_data = [
    1, 5, 4, 2, 3, 5, 4, 2, 3, 6, 5, 3
]

bear_trap_data = [
    2, 9, 8, 2, 3, 7, 6, 2, 3, 5, 4, 1, 2, 4
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
    traps = chart.get_traps()

    assert traps == {}

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
    traps = chart.get_traps()

    assert traps == {}