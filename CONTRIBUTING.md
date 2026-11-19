# Contributing to pacelab

Thanks for helping. Bug reports, file-format edge cases, metric ideas and code are all welcome.

## Set up

```bash
uv sync
make check
```

`make check` runs ruff, mypy (strict) and the test suite. CI runs the same command.

## Reporting a parsing bug

The most useful report includes the file that fails. Activity files contain GPS tracks, so strip or shift the positions first, or describe the device, firmware and export path so we can reproduce it with a generated file.

## Changing a metric

Metric definitions are part of the public contract. A change needs:

1. The definition updated in `GLOSSARY.md`.
2. A test in `packages/pacelab/tests/test_metrics.py` with hand-computed expected values, seen failing before the change.
3. A note in the pull request on how results shift for existing users.

## Pull requests

- One concern per pull request.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): `feat(metrics): add grade-adjusted pace`.
- UI changes include before and after screenshots.
- New decisions that are hard to reverse get an ADR in `docs/adr/`.

By contributing you agree that your contributions are licensed under the Apache License 2.0.
