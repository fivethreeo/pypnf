"""Price projections following du Plessis, chapter 4 (printed pp. 207-252).

Pattern selection is subjective. Automatic counts are candidates, not an
exhaustive identification of significant tops, bottoms, or congestion areas.
"""

import math
import operator

import numpy as np


def _index(value, size, name):
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be an integer index.")
    try:
        value = operator.index(value)
    except TypeError:
        raise ValueError(f"{name} must be an integer index.") from None
    if not 0 <= value < size:
        raise ValueError(f"{name} must be between 0 and {size - 1}.")
    return value


def _first(mask):
    indices = np.flatnonzero(mask)
    return int(indices[0]) if len(indices) else None


class _Counts:
    def __init__(self, chart):
        if chart.scaling not in ("abs", "log"):
            raise NotImplementedError("Price counts require absolute or logarithmic scaling.")
        if chart.reversal < 1 or int(chart.reversal) != chart.reversal:
            raise ValueError("Price counts require a positive integer reversal.")
        self.matrix = chart.matrix
        self.scale = chart.boxscale
        self.boxsize = float(chart.boxsize)
        self.scaling = chart.scaling
        self.reversal = int(chart.reversal)
        occupied = self.matrix != 0
        if not np.all(np.any(occupied, axis=0)):
            raise ValueError("Price counts require populated chart columns.")
        self.low = np.argmax(occupied, axis=0)
        self.high = len(self.scale) - 1 - np.argmax(occupied[::-1], axis=0)
        self.direction = self.matrix[self.high, np.arange(self.matrix.shape[1])]
        self.mixed = np.any(self.matrix == 1, axis=0) & np.any(self.matrix == -1, axis=0)
        self.size = self.matrix.shape[1]

        ts = chart.pnf_timeseries
        columns = np.asarray(ts["column index"])
        rows = np.asarray(ts["box index"])
        valid = np.isfinite(columns) & np.isfinite(rows)
        columns, rows = columns[valid].astype(int), rows[valid].astype(int)
        changed = np.r_[True, (np.diff(columns) != 0) | (np.diff(rows) != 0)]
        self.event_columns = columns[changed]
        self.event_rows = rows[changed]

    def _project(self, anchor, boxes, direction):
        if self.scaling == "log":
            return anchor * math.exp(direction * boxes * math.log1p(self.boxsize / 100))
        return anchor + direction * boxes * self.boxsize

    def _price(self, row):
        if 0 <= row < len(self.scale):
            return float(self.scale[row])
        edge = 0 if row < 0 else len(self.scale) - 1
        return self._project(float(self.scale[edge]), abs(row - edge), 1 if row > edge else -1)

    def _result(self, kind, method, start, end, count, anchor, direction,
                trigger, negate, established, reason):
        target = self._project(self._price(anchor), count * self.reversal, direction)
        result = {
            "type": kind,
            "method": method,
            "trend": int(direction),
            "start column": int(start),
            "end column": int(end),
            "box index": int(anchor),
            "count": int(count),
            "anchor": self._price(anchor),
            "target": target,
            "activation": self._price(trigger),
            "negation": self._price(negate),
            "reason": reason,
            "status": "established",
            "established column": int(established),
            "activated column": None,
            "achieved column": None,
            "negated column": None,
        }
        first = np.searchsorted(self.event_columns, established)
        rows = self.event_rows[first:]
        columns = self.event_columns[first:]
        activation = _first(direction * (rows - trigger) >= 0)
        negation = _first(direction * (rows - negate) <= 0)
        if activation is not None and (negation is None or activation < negation):
            result["activated column"] = int(columns[activation])
            result["status"] = "active"
            end_event = len(rows) if negation is None else negation
            prices = self.scale[rows[activation:end_event]]
            achievement = _first(direction * (prices - target) >= 0)
            if achievement is not None:
                result["achieved column"] = int(columns[activation + achievement])
                result["status"] = "achieved"
                return result
        if negation is not None:
            result["negated column"] = int(columns[negation])
            result["status"] = "negated"
        return result

    def _multi_box(self):
        if self.reversal == 1:
            raise ValueError("One-box charts support horizontal activity counts, not vertical or Cohen counts.")
        if np.any(self.mixed):
            raise ValueError("Multi-box counts require single-direction columns.")

    def vertical(self, column, reason="explicit selection"):
        self._multi_box()
        column = _index(column, self.size, "column")
        if column == 0 or column == self.size - 1:
            raise ValueError("A vertical count needs a preceding column and a completed counting column.")
        direction = int(self.direction[column])
        if self.direction[column - 1] != -direction:
            raise ValueError("The preceding column must have the opposite direction.")
        anchor = self.low[column - 1] if direction == 1 else self.high[column - 1]
        trigger = self.high[column] + 1 if direction == 1 else self.low[column] - 1
        count = np.count_nonzero(self.matrix[:, column])
        return self._result(
            "vertical", "thrust", column, column, count, anchor, direction,
            trigger, anchor - direction, column + 1, reason,
        )

    def cohen(self, start, end, reason="explicit selection"):
        self._multi_box()
        start = _index(start, self.size, "start_column")
        end = _index(end, self.size, "end_column")
        if end - start < 3:
            raise ValueError("A Cohen count needs opposite entry/exit walls and intervening congestion.")
        direction = int(self.direction[end])
        if self.direction[start] != -direction:
            raise ValueError("Cohen counts require opposite-direction entry and exit walls.")
        interior = np.arange(start + 1, end)
        matching = interior[self.direction[interior] == direction]
        if not len(matching):
            raise ValueError("The pattern needs an interior column in the breakout direction.")
        if direction == 1:
            trigger = int(np.max(self.high[matching])) + 1
            anchor = int(np.min(self.low[start:end + 1]))
        else:
            trigger = int(np.min(self.low[matching])) - 1
            anchor = int(np.max(self.high[start:end + 1]))
        if not (self.low[start] <= trigger <= self.high[start]
                and self.low[end] <= trigger <= self.high[end]):
            raise ValueError("Both walls must reach the breakout row beyond the interior congestion.")
        if np.any(self.matrix[trigger, start + 1:end]):
            raise ValueError("The breakout row must be clear between the entry and exit walls.")
        return self._result(
            "horizontal", "cohen", start, end, end - start + 1, anchor,
            direction, trigger, anchor - direction, end, reason,
        )

    def wall_patterns(self):
        self._multi_box()
        last = np.full(len(self.scale), -1, dtype=int)
        patterns = []
        for end in range(self.size):
            rows = np.flatnonzero(self.matrix[:, end])
            candidates = np.unique(last[rows])
            for start in candidates:
                if start < 0 or end - start < 3 or self.direction[start] == self.direction[end]:
                    continue
                try:
                    self.cohen(int(start), end)
                except ValueError:
                    continue
                patterns.append((int(start), end))
            last[rows] = end
        return patterns

    def activity(self, start, end, row=None):
        start = _index(start, self.size, "start_column")
        end = _index(end, self.size, "end_column")
        if end - start < 2:
            raise ValueError("An activity count needs at least three columns of congestion.")
        pattern = self.matrix[:, start:end + 1] != 0
        activity = np.count_nonzero(pattern, axis=1)
        if row is None:
            candidates = np.flatnonzero(activity == np.max(activity))
            if len(candidates) != 1:
                raise ValueError("Several rows have equal maximum activity; choose count_row explicitly.")
            row = int(candidates[0])
        else:
            row = _index(row, len(self.scale), "count_row")
        filled = np.flatnonzero(pattern[row])
        if len(filled) < 2:
            raise ValueError("The counting row must cross at least two populated columns.")
        count = int(filled[-1] - filled[0] + 1)
        low = int(np.min(self.low[start:end + 1]))
        high = int(np.max(self.high[start:end + 1]))
        results = []
        for direction in (1, -1):
            trigger = high + 1 if direction == 1 else low - 1
            negate = low - 1 if direction == 1 else high + 1
            result = self._result(
                "horizontal", "activity", start, end, count, row, direction,
                trigger, negate, end + 1, "explicit congestion range and counting row",
            )
            result["count start column"] = start + int(filled[0])
            result["count end column"] = start + int(filled[-1])
            # The range is known now; subsequent columns determine its breakout.
            result["established column"] = end
            results.append(result)
        return results

    def vertical_candidates(self):
        self._multi_box()
        exits = {end for _, end in self.wall_patterns()}
        results = []
        for column in range(1, self.size - 1):
            direction = self.direction[column]
            extreme = self.low if direction == 1 else -self.high
            reason = None
            if column >= 3 and extreme[column - 1] < extreme[column - 3]:
                reason = "first thrust after a new local extreme"
            elif (column >= 5
                  and extreme[column - 3] < extreme[column - 5]
                  and 0 <= extreme[column - 1] - extreme[column - 3] <= 1
                  and self.high[column - 2] - self.low[column - 2] + 1 <= self.reversal + 1):
                reason = "second thrust after a short first column"
            elif column in exits:
                reason = "congestion wall breakout"
            if reason:
                results.append(self.vertical(column, reason))
        return results


def vertical_counts(chart, column=None):
    counts = _Counts(chart)
    return counts.vertical_candidates() if column is None else [counts.vertical(column)]


def horizontal_counts(chart, start_column=None, end_column=None, method=None, count_row=None):
    counts = _Counts(chart)
    if method is None:
        method = "activity" if chart.reversal == 1 else "cohen"
    if method not in ("cohen", "activity"):
        raise ValueError("method must be 'cohen' or 'activity'.")
    if method == "cohen" and count_row is not None:
        raise ValueError("count_row is only used by activity counts.")
    if start_column is None and end_column is None:
        if method != "cohen":
            raise ValueError("Activity counts require explicit start_column and end_column.")
        return [counts.cohen(start, end, "congestion wall breakout")
                for start, end in counts.wall_patterns()]
    if start_column is None or end_column is None:
        raise ValueError("Specify both start_column and end_column.")
    if method == "activity":
        return counts.activity(start_column, end_column, count_row)
    return [counts.cohen(start_column, end_column)]
