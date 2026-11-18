
![logo](https://github.com/swaschke/pypnf/blob/main/images/logo.png)

### A Python Package for Point & Figure Charting

[![license](https://img.shields.io/github/license/swaschke/pypnf)](#license)
[![Python Version](https://img.shields.io/pypi/pyversions/pypnf?style=flat)](https://pypi.org/project/pypnf/)
[![PyPi Version](https://img.shields.io/pypi/v/pypnf?style=flat)](https://pypi.org/project/pypnf/)
[![Package Status](https://img.shields.io/pypi/status/pypnf?style=flat)](https://pypi.org/project/pypnf/)

<hr>

### Installation
```python
pip install pypnf
```

<hr>

### Usage

#### Quickstart using integrated time-series example


```python
from pypnf import PointFigureChart
from pypnf import dataset

symbol = 'AAPL'  # or 'MSFT'

ts = dataset(symbol)

pnf = PointFigureChart(ts=ts, method='cl', reversal=2, boxsize=5, scaling='abs', title=symbol)

print(pnf)
```

```
Point & Figure (abs|cl) 5 x 2 | AAPL
---  -  -  -  -  -  -  -  ---
135  .  .  .  .  .  .  X  135
130  .  .  X  .  .  .  X  130
125  .  .  X  O  .  .  X  125
120  .  .  X  O  X  .  X  120
115  .  .  X  O  X  O  X  115
110  .  .  X  O  .  O  .  110
105  .  .  X  .  .  .  .  105
100  .  .  X  .  .  .  .  100
 95  .  .  X  .  .  .  .   95
 90  .  .  X  .  .  .  .   90
 85  .  .  X  .  .  .  .   85
 80  X  .  X  .  .  .  .   80
 75  X  O  X  .  .  .  .   75
 70  .  O  X  .  .  .  .   70
 65  .  O  X  .  .  .  .   65
 60  .  O  .  .  .  .  .   60
---  -  -  -  -  -  -  -  ---
printed 7/7 columns.
```

##### Plotting Point&Figure Charts

```python
from pypnf import PointFigureChart
from pypnf import dataset

data = dataset('^SPX')

pnf = PointFigureChart(ts=data, method='h/l', reversal=2, boxsize=50, scaling='abs', title='^SPX')
pnf.bollinger(5, 2)
pnf.donchian(8,2)
pnf.psar(0.02, 0.2)
pnf.show()
# or
pnf.write_html('chart.html')
```

HTML exports are standalone Canvas charts with mouse, touch, and keyboard pan/zoom.
Use **Latest 50** or **Fit all** to reset the view, and the checkboxes to toggle
gridlines, external trendlines, breakouts, and individual indicators.
Only visible boxes and axis labels are drawn; no SVG nodes are created per box.
**Grid only** enables the grid and hides all overlays, retaining the X/O price
symbols. Vertical and horizontal active count targets have separate toggles;
**Fit targets** includes enabled target levels outside the current price range.
**Achieved targets** is off by default and independently shows historical counts
of both types as muted lines, ending in diamonds at the columns where they were
reached. Click a line or diamond to see the achievement column and its date.
Blue triangles mark each enabled target's activation threshold at its recorded
activation column, even when the projected target is off-screen. Hover a
triangle, target line, or label to outline the activation column in blue and
trace a dashed connector from the activation price to the projection.
While a target is hovered, a one-device-pixel horizontal hairline connects its
activation price to the price axis, even if its activation column is off-screen
to the left. The hairline disappears when the pointer leaves the target, including
when its clicked info card remains open.
Hover only highlights; click a line, label or marker to open its info card.
The info card identifies activations outside the view or omitted by export trimming.
V+/V- and H+/H- labels identify upside/downside projections. Nearby labels are
grouped with their count; `~` marks an approximate grouped price. Hover over a
target line or label to highlight its counting columns and show their original,
1-based column numbers. Clicking opens a multiline info card, not a hover tooltip,
showing the exact target price, method, count calculation, anchor, source dates,
activation and negation details. Scroll the card to inspect overlapping targets;
use **Close**, click empty chart space, or press **Escape** to dismiss it.
The card stays open while you move the pointer. Use **Drag to move** to reposition
it with a mouse or touch; the focused handle also supports arrow keys. The card
stays within the visible chart, and its contents scroll independently of dragging.
A vertical target highlights its counting column; a
horizontal target highlights its full counting range. Off-screen sources are
identified as left/right of the view; use **Fit all** or pan to find them.
Sources removed by export trimming are marked as omitted rather than highlighted
in the empty grid.

Chart data is stored as compact column ranges in gzip-compressed, Base64-encoded
JSON and decompressed locally in the browser. No server, CDN, or JavaScript
dependencies are required. Open the file in a current browser supporting Canvas,
Pointer Events, ResizeObserver, and `DecompressionStream` (current Chrome, Edge,
Firefox, and Safari). Compression reduces file size; it does not encrypt the data.

The `date_format` and `template` arguments to `write_html()` remain available.
Custom templates based on the previous SVG template are still supported. New
templates can use `pypnf/html/canvas.html` as their starting point; its
`__PYPNF_CHART_DATA__` marker is replaced by the compressed Base64 payload.

![chart](https://github.com/swaschke/pypnf/blob/main/images/chart.png)

#### Price-target counts

Vertical and horizontal targets follow the counting rules in chapter 4 of Jeremy
du Plessis's *The Definitive Guide to Point and Figure* (pp. 207-252):

```python
vertical = pnf.get_vertical_counts()
horizontal = pnf.get_horizontal_counts()

for count in vertical + horizontal:
    if count['status'] == 'active':
        print(count['type'], count['trend'], count['target'])
```

Both methods return lists of dictionaries and also support explicit selection:
`get_vertical_counts(column=...)` selects a completed counting column;
`get_horizontal_counts(start_column=..., end_column=...)` selects a congestion
pattern, including both walls. All row and column indices are **zero-based** and
refer to the original chart matrix, not a trimmed plot.

Vertical targets count all boxes in the chosen column and anchor to the preceding
O column's low (upside) or X column's high (downside). A reversal fixes the count;
a subsequent break beyond the counting column activates it. Horizontal **Cohen**
counts require opposite-direction entry and exit walls, intervening congestion,
and a clear breakout row joining both walls. Their inclusive pattern width
determines the count, anchored to the pattern's low or high; establishment and
activation occur together on the exit breakout.

Arithmetic projections add/subtract `count * boxsize * reversal` from the anchor.
Logarithmic projections use `anchor * (1 + boxsize / 100) ** (+/-count * reversal)`,
not an arithmetic percentage approximation. ATR charts use their resolved
absolute box size. Classic variable-box scales (`cla`) are not supported.

Each result includes `count`, `anchor`, `target`, `trend` (+1/-1), `activation`,
`negation`, `reason`, and `status` (`established`, `active`, `achieved`, or
`negated`), plus the corresponding event-column indices. `box index` is the
anchor row. A break beyond the anchor negates an unfulfilled vertical/Cohen
count. Achievement is terminal; a later reversal does not undo a reached target.

Automatic results are **candidates requiring analyst judgment**, including
countertrend candidates, not an instruction to count every column. Vertical
selection looks for first thrusts after new local lows/highs, second thrusts
within one box of the first anchor after a short first column, and congestion
wall breakouts. For this heuristic, “short” means at most `reversal + 1` boxes.
Horizontal selection searches for clear Cohen wall breakouts, including nested
patterns. These heuristics cannot identify every subjectively significant
top/bottom. Explicit vertical selection validates completion and direction, not
the analyst's assessment of significance.

For **one-box charts**, use an explicit congestion range with
`get_horizontal_counts(start_column=..., end_column=..., method='activity')`.
This counts the span of the most populated row, including empty cells between its
first and last filled boxes, and projects both upside and downside from that row.
If several rows tie, supply `count_row=...`; this also allows selecting a counting
row manually. The two projections remain unactivated until a later column breaks
out of the selected range. A breakout in one direction negates the opposing
projection. The same row-based method is available on multi-box charts as the
De Villiers/Taylor alternative. Automatic activity-range selection and vertical
one-box counts are intentionally not offered. Multi-box counts use the chart's
actual reversal (the book's main examples use three).

Counts are computed on demand without changing chart signals or plotting state.
Canvas exports include automatic **active** and **achieved** targets on supported
multi-box absolute/log charts, omitting established-only and negated counts.
Achieved targets remain hidden until their checkbox is enabled.
PNG charts are unchanged. One-box and classic-scale Canvas charts still export,
but do not include automatic targets.
Targets have no implied time horizon or guarantee of achievement.

#### Quickstart using time-series data loaded via the external package yfinance

If the yfinance and/or pandas package is not yet installed use:

```python
pip install pandas
pip install yfinance
```

In order to process the downloaded data with the PointFigureChart-class the time-series data needs to be  prepared.

```python
import yfinance as yf

symbol = 'AAPL'

data = yf.Ticker(symbol)
ts = data.history(start='2018-01-01', end='2018-06-30')

# reset index
ts.reset_index(level=0, inplace=True)

# convert pd.timestamp to string
ts['Date'] = ts['Date'].dt.strftime('%Y-%m-%d')

# select required keys
ts = ts[['Date','Open','High','Low','Close']]

# convert DataFrame to dictionary
ts = ts.to_dict('list')
```

Initiate the PointFigureChart object with the prepared data and chart parameter, 
get the trendlines and print the resulting Point and Figure Chart.

```python
from pypnf import PointFigureChart

pnf = PointFigureChart(ts=ts, method='cl', reversal=3, boxsize=2, scaling='abs', title='AAPL')
pnf.get_trendlines()
print(pnf)
```

```
Point & Figure (abs|cl) 2 x 3 | AAPL
--  -  -  -  -  -  -  -  -  -  -  -  --
90  .  .  .  .  .  .  .  .  .  .  X  90
88  .  .  .  .  .  .  .  .  .  .  X  88
86  .  .  .  .  .  .  .  .  .  .  X  86
84  .  .  .  .  .  .  .  .  .  .  X  84
82  .  .  .  .  .  .  .  .  .  .  X  82
80  .  .  .  .  X  .  .  .  .  .  X  80
78  .  .  .  .  X  O  .  .  .  .  X  78
76  .  .  .  .  X  O  .  .  .  .  X  76
74  .  .  .  .  X  O  X  .  .  .  X  74
72  .  .  .  .  X  O  X  O  .  .  X  72
70  .  .  .  .  X  O  X  O  .  .  X  70
68  .  .  .  .  X  O  .  O  X  .  X  68
66  .  .  .  .  X  .  .  O  X  O  X  66
64  .  .  .  .  X  .  .  O  X  O  X  64
62  .  .  .  .  X  .  .  O  .  O  X  62
60  .  .  .  .  X  .  .  .  .  O  X  60
58  *  .  .  .  X  .  .  .  .  O  X  58
56  X  *  .  .  X  .  .  .  .  O  .  56
54  X  O  *  .  X  .  .  .  .  .  .  54
52  X  O  .  *  X  .  .  .  .  .  *  52
50  X  O  X  .  X  .  .  .  .  *  .  50
48  X  O  X  O  X  .  .  .  *  .  .  48
46  X  O  X  O  X  .  .  *  .  .  .  46
44  X  O  X  O  .  .  *  .  .  .  .  44
42  X  O  X  .  .  *  .  .  .  .  .  42
40  X  O  X  .  *  .  .  .  .  .  .  40
38  .  O  X  *  .  .  .  .  .  .  .  38
36  .  O  *  .  .  .  .  .  .  .  .  36
--  -  -  -  -  -  -  -  -  -  -  -  --
last trendline: bullish support line of length 10
printed 11/11 columns.
```

<hr>

<h3>Literature</h3>

**Weber, Zieg (2003)** The Complete Guide to Point-and-Figure Charting - The new science of an old art. <i>Harriman House</i>, ISBN: 1-897-5972-82<br>

**du Plessis (2012)** The Definitive Guide to Point and Figure: A Comprehensive Guide to the Theory and Practical Use of the Point and Figure Charting Method. 2nd Edition. <i>Harriman House</i>, ISBN: 978-0857192455<br> 

**du Plessis (2015)** 21st Century Point and Figure - New and advanced techniques for using Point and Figure charts. <i>Harriman House</i>, ISBN: 978-0857194428<br>

**Shah (2018)** Trading the Markets the Point & Figure way : become a noiseless trader and achieve consistent success in markets. <i>Notion Press</i>, ISBN:  978-1642492248<br> 

<hr>

<h3>Copyright</h3>
pyPnF is licensed under a GNU General Public License v2 (GPLv2).

