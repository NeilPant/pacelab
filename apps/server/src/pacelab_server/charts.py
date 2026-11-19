from dataclasses import dataclass

import polars as pl

WIDTH = 720
HEIGHT = 160
INSET = 12
MAX_POINTS = 600


@dataclass(frozen=True, slots=True)
class Series:
    path: str
    low: float
    high: float


def series(records: pl.DataFrame, column: str, invert: bool = False) -> Series | None:
    if column == "pace":
        frame = records.filter(pl.col("speed") > 0.5).select(
            "distance", pace=1000 / pl.col("speed")
        )
    else:
        frame = records.select("distance", column).drop_nulls()
    if frame.height < 2:
        return None
    step = max(1, frame.height // MAX_POINTS)
    frame = frame.gather_every(step)
    x = frame["distance"].to_list()
    y = frame[column].to_list()
    x0, x1 = x[0], x[-1]
    low, high = min(y), max(y)
    span_x = (x1 - x0) or 1.0
    span_y = (high - low) or 1.0
    points = []
    for xi, yi in zip(x, y, strict=True):
        fraction = (yi - low) / span_y
        top = fraction if invert else 1 - fraction
        y_px = INSET + top * (HEIGHT - 2 * INSET)
        points.append(f"{(xi - x0) / span_x * WIDTH:.1f},{y_px:.1f}")
    return Series(path="M" + " L".join(points), low=low, high=high)
