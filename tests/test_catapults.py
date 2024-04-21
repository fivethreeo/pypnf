from pypnf import PointFigureChart


bullish_catapult_data = [
   4, 2, 1, 5, 2, 1, 5, 2, 6, 3, 7
]

bearish_catapult_data = [
    4, 6, 3, 6, 3, 6, 2, 5, 1
]

def test_bullish_catapult():
    chart = PointFigureChart(
        {"close": bullish_catapult_data},
        "cl",
        3,
        1,
        "abs",
        "test_bullish_catapult"
    )
    chart.show()
    catapults = chart.get_catapults()

    assert catapults == {}

def test_bearish_catapult():
    chart = PointFigureChart(
        {"close": bearish_catapult_data},
        "cl",
        3,
        1,
        "abs",
        "test_bearish_catapult"
    )
    chart.show()
    catapults = chart.get_catapults()

    assert catapults == {}