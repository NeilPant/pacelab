# pacelab

Parse sports-watch activity files (FIT, GPX, TCX) into one normalised record stream and compute running metrics.

```bash
pip install pacelab
```

```python
from pacelab import load
from pacelab.metrics import best_efforts, summarize

activity = load("morning.fit")
print(summarize(activity))
print(best_efforts(activity))
```

```bash
pacelab summary morning.fit
pacelab efforts morning.fit
pacelab export morning.fit records.parquet
```

See the [project README](https://github.com/tanhtruong/pacelab) for the full documentation.
