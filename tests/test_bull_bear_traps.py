from pypnf import PointFigureChart

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
    # chart.show()
    traps = chart.get_traps()

    assert traps == {
        'bottom box index': [
            2.0,
        ],
        'box index': [
            4.0,
        ],
        'column index': [
            5,
        ],
        'top box index': [
            7.0,
        ],
        'trend': [
            -1,
        ],
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
    # chart.show()
    traps = chart.get_traps()

    assert traps == {
        'bottom box index': [
            3.0,
        ],
        'box index': [
            6.0,
        ],
        'column index': [
            6,
        ],
        'top box index': [
            11.0,
        ],
        'trend': [
            1,
        ],
    }
