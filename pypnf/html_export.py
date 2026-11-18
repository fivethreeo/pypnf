"""Standalone HTML export, independent of Matplotlib's figure preparation."""

import base64
import datetime
import gzip
import json
import math
import re
from importlib.resources import files
from pathlib import Path

import numpy as np


DATA_MARKER = "__PYPNF_CHART_DATA__"


def _json_value(value, date_format, strict=True):
    if isinstance(value, np.datetime64):
        return value.astype("datetime64[us]").item().strftime(date_format)
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.strftime(date_format)
    if isinstance(value, np.ndarray):
        return [_json_value(item, date_format, strict) for item in value]
    if isinstance(value, np.generic):
        return _json_value(value.item(), date_format, strict)
    if isinstance(value, dict):
        return {key: _json_value(item, date_format, strict) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item, date_format, strict) for item in value]
    if strict and isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _dumps(value, date_format, strict=True):
    return json.dumps(
        _json_value(value, date_format, strict),
        allow_nan=not strict,
        separators=(",", ":"),
    ).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def _prepare_data(chart):
    offset = 0
    if chart.cut2indicator and chart.indicator:
        for values in chart.indicator.values():
            valid = np.flatnonzero(np.isfinite(values))
            if not len(valid):
                raise ValueError("Cannot trim a chart to an indicator with no finite values.")
            offset = max(offset, int(valid[0]))

    matrix = chart.matrix[:, offset:]
    occupied = np.flatnonzero(np.any(matrix != 0, axis=1))
    if not len(occupied):
        raise ValueError("Cannot export a chart with no populated boxes.")
    bottom = max(0, int(occupied[0]) - 3)
    top = min(len(chart.boxscale), int(occupied[-1]) + 4)
    matrix = matrix[bottom:top]

    indicators = {}
    for key, values in chart.indicator.items():
        values = values[offset:]
        if "pSAR" in key:
            indicators[key] = (
                chart._coordinates2plot_grid(np.abs(values)) - bottom
            ) * np.sign(values)
        else:
            indicators[key] = chart._coordinates2plot_grid(values) - bottom

    labels = chart.column_labels
    if labels is None:
        labels = [str(index + 1) for index in range(chart.matrix.shape[1])]
    return {
        "title": chart.title,
        "scaling": chart.scaling,
        "boxSize": chart.boxsize,
        "matrix": matrix,
        "boxScale": chart.boxscale[bottom:top],
        "columnLabels": labels[offset:],
        "indicators": indicators,
        "trendLines": chart.trendlines if chart.trendlines is not None else chart.get_trendlines(),
        "breakOuts": chart.breakouts if chart.breakouts is not None else chart.get_breakouts(),
        "matrix_bottom_cut_index": bottom,
        "matrix_top_cut_index": top,
        "columnOffset": offset,
    }


def _column_runs(matrix):
    """Encode each contiguous, same-sign column segment as [start, stop, sign]."""
    columns = []
    for column in matrix.T:
        boundaries = np.flatnonzero(np.diff(np.r_[0, column, 0]))
        columns.append([
            [int(start), int(stop), int(column[start])]
            for start, stop in zip(boundaries, boundaries[1:])
            if column[start] != 0
        ])
    return columns


def _price_targets(chart):
    if chart.scaling not in ("abs", "log") or chart.reversal < 2:
        return []
    counts = chart.get_vertical_counts() + chart.get_horizontal_counts()
    return [count for count in counts if count["status"] in ("active", "achieved")]


def write_html(chart, fname, date_format, template):
    html = (
        Path(template).read_text(encoding="utf-8")
        if template is not None
        else files("pypnf").joinpath("html/canvas.html").read_text(encoding="utf-8")
    )
    data = _prepare_data(chart)
    if DATA_MARKER in html:
        data["columns"] = _column_runs(data.pop("matrix"))
        data["targets"] = _price_targets(chart)
        data["reversal"] = chart.reversal
        compressed = gzip.compress(_dumps(data, date_format).encode("utf-8"), mtime=0)
        html = html.replace(DATA_MARKER, base64.b64encode(compressed).decode("ascii"), 1)
    else:
        # Preserve the declaration-based contract of existing custom SVG templates.
        offset = data.pop("columnOffset")
        for key in ("trendLines", "breakOuts"):
            data[key] = dict(data[key])
            data[key]["column index"] = np.asarray(data[key]["column index"]) - offset
        for name, value in data.items():
            pattern = rf"\blet {name} = .*?;"
            replacement = f"let {name} = {_dumps(value, date_format, strict=False)};"
            html, count = re.subn(pattern, lambda match: replacement, html, count=1, flags=re.DOTALL)
            if count != 1:
                raise ValueError(f"Custom template is missing a declaration for {name}.")
    Path(fname).write_text(html, encoding="utf-8")
