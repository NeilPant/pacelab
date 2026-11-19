import datetime as dt
import math

import pytest
from pacelab import Activity, Sport
from pacelab.metrics import (
    aerobic_decoupling,
    best_efforts,
    elevation_change,
    summarize,
    time_in_zones,
    training_load,
    trimp,
)

START = dt.datetime(2026, 3, 1, 7, 0, tzinfo=dt.UTC)


def run(rows):
    return Activity.from_rows(
        [{"timestamp": START + dt.timedelta(seconds=r.pop("t")), **r} for r in rows],
        sport=Sport.RUNNING,
    )


def steady(seconds, speed, start_t=0.0, start_d=0.0, **extra):
    return [
        {"t": start_t + i, "distance": start_d + i * speed, **extra} for i in range(seconds + 1)
    ]


def test_summary_counts_only_moving_time():
    rows = steady(600, 3.0)
    rows += [{"t": 600.0 + i, "distance": 1800.0} for i in range(1, 61)]
    rows += steady(300, 3.0, start_t=720.0, start_d=1800.0)[0:]

    summary = summarize(run(rows))

    assert summary.distance_m == 2700.0
    assert summary.elapsed_s == 1020.0
    assert summary.moving_s == 900.0
    assert summary.pace_s_per_km == pytest.approx(900 / 2.7)


def test_elevation_change_ignores_noise_below_threshold():
    altitudes = [100, 101, 100, 99, 101, 100]
    altitudes += [*range(101, 121), 119, 120]
    altitudes += [*range(119, 109, -1), 111]

    assert elevation_change(altitudes, threshold_m=3.0) == (20.0, 10.0)


def test_best_efforts_interpolate_and_skip_distances_longer_than_the_run():
    rows = steady(250, 4.0)
    rows += steady(200, 5.0, start_t=250.0, start_d=1000.0)[1:]
    rows += steady(125, 4.0, start_t=450.0, start_d=2000.0)[1:]

    efforts = best_efforts(run(rows), distances_m=(400.0, 1000.0, 1609.344, 5000.0))

    assert efforts == pytest.approx({400.0: 80.0, 1000.0: 200.0, 1609.344: 352.336})


def test_time_in_zones_splits_recorded_time_by_heart_rate():
    rows = steady(99, 3.0, heart_rate=120)
    rows += steady(200, 3.0, start_t=100.0, start_d=300.0, heart_rate=130)

    assert time_in_zones(run(rows), boundaries_bpm=(130, 160)) == [100.0, 200.0, 0.0]


def test_trimp_follows_banister_formula():
    rows = steady(3600, 3.0, heart_rate=125)

    expected = 60 * 0.5 * 0.64 * math.exp(1.92 * 0.5)
    assert trimp(run(rows), resting_hr=50, max_hr=200) == pytest.approx(expected)


def test_aerobic_decoupling_compares_efficiency_of_both_halves():
    rows = steady(1000, 3.0, heart_rate=140)
    rows += steady(1000, 3.0, start_t=1001.0, start_d=3003.0, heart_rate=147)

    assert aerobic_decoupling(run(rows)) == pytest.approx((1 - 140 / 147) * 100, abs=0.01)


def test_training_load_fills_rest_days_and_reports_form_going_into_the_day():
    day0 = dt.date(2026, 3, 1)

    frame = training_load({day0: 100.0}, start=day0, end=day0 + dt.timedelta(days=1))

    assert frame["date"].to_list() == [day0, day0 + dt.timedelta(days=1)]
    assert frame["load"].to_list() == [100.0, 0.0]
    assert frame["fitness"].to_list() == pytest.approx([100 / 42, 100 / 42 * 41 / 42])
    assert frame["fatigue"].to_list() == pytest.approx([100 / 7, 100 / 7 * 6 / 7])
    assert frame["form"].to_list() == pytest.approx([0.0, 100 / 42 - 100 / 7])
