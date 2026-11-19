# Glossary

**Activity** - One recorded workout: its sport, start time, source device and record stream. Built by `pacelab.load` from a file, or by `Activity.from_rows`.

**Record stream** - The per-sample telemetry of an activity, a polars DataFrame with the canonical columns and units listed in the README. Every source format is normalised into it; nothing downstream knows which format a file came from.

**Source format** - The file type an activity was read from: `fit`, `gpx` or `tcx`.

**Interval** - The span between two consecutive records. Metrics are computed over intervals, not samples: an interval's duration and distance are the differences between its two records, and its heart rate, cadence and power are those of its first record.

**Recording interval** - An interval no longer than 30 s. A longer gap means the watch was paused or lost signal; it counts toward elapsed time and nothing else.

**Moving interval** - A recording interval covered at 0.5 m/s or faster.

**Moving time** - The summed duration of moving intervals.

**Elapsed time** - Last record's time minus first record's time.

**Pace** - Moving time per kilometre.

**Grade-adjusted pace (GAP)** - Equivalent flat-ground moving pace, in seconds per kilometre, for running sports. Uses the running energy-cost model from [Minetti et al. (2002), Figure 1](https://doi.org/10.1152/japplphysiol.01177.2001):

```text
C(g) = 155.4*g^5 - 30.4*g^4 - 43.3*g^3 + 46.3*g^2 + 19.5*g + 3.6
equivalent_distance = sum(interval_distance * C(g) / C(0))
GAP = sum(moving_seconds) * 1000 / equivalent_distance
```

Here `g` is elevation change divided by recorded distance (a ratio, not percent); uphill is positive. Grade is the elevation difference across a centered 30 m distance window divided by that window's length, with elevations interpolated between records. Windows shorten at the ends of each moving block, preserving a constant slope even in short activities or irregular samples. They never cross stationary intervals or recording gaps. Grades are clamped to the study's -45% to +45% range to avoid extrapolating the polynomial.

Only moving intervals contribute time and equivalent distance. Missing or nonfinite elevation at either endpoint of any moving interval makes GAP unavailable (`None`), as do non-running sports and activities with no moving time. The value is an estimate of metabolic equivalence, not a prediction of downhill speed, and is not intended to reproduce a proprietary platform's GAP. Existing pace, climb and other summary fields are unchanged.

**Cadence** - Steps per minute, both feet. FIT, GPX and TCX files store running cadence per foot; the parsers double it.

**Climb** (elevation gain) - Ascent with altitude noise filtered out: a rise or fall counts only once it reaches 3 m from the last turning point.

**Best effort** - The fastest time over a fixed distance anywhere within an activity, interpolated between samples.

**Heart-rate zone** - A heart-rate band bounded by user-chosen thresholds. A heart rate equal to a threshold belongs to the higher zone.

**TRIMP** - Banister's training impulse: minutes weighted by heart-rate reserve, a single number for how hard a session was.

**Aerobic decoupling** - How much efficiency (speed per heartbeat) fell from the first half of the moving time to the second, as a percentage. Under 5 % on a long steady run is read as good aerobic endurance.

**Training load** - Daily stress numbers (for example TRIMP per day) fed into the fitness/fatigue model.

**Fitness** - 42-day exponentially weighted average of training load (often called CTL).

**Fatigue** - 7-day exponentially weighted average of training load (often called ATL).

**Form** - Fitness minus fatigue as it stood at the start of the day, before that day's training (often called TSB).
