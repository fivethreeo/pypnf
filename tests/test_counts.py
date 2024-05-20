from pypnf import PointFigureChart
from pypnf import dataset

def test_counts_abs():
    symbol = 'AAPL'  # or 'MSFT'

    ts = dataset(symbol)

    pnf = PointFigureChart(ts=ts, method='cl', reversal=2, boxsize=5, scaling='abs', title=symbol)
    counts = pnf.get_counts()

    assert counts == {}