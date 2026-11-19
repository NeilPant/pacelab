# 2. Parse FIT with fitdecode, not Garmin's SDK

Date: 2026-11-19

## Status

Accepted

## Context

Garmin publishes an official Python FIT SDK (`garmin-fit-sdk`). It is well maintained, but it is licensed under Garmin's own FIT Protocol License: a non-transferable, non-sublicensable licence for the licensee's "internal business purposes". That is not an OSI-approved open source licence, and it is unclear how it applies to an Apache-2.0 project whose users redistribute it.

`fitdecode` is MIT-licensed, pure Python, decodes every message in the FIT profile, checks CRCs, and applies scale, offset and units.

## Decision

Use `fitdecode` for FIT decoding. Tests generate FIT fixtures with `fit-tool` (BSD-3-Clause, a dev dependency only), so the repository contains no binary files with unclear origin.

## Consequences

- No licence ambiguity for users or redistributors.
- `fitdecode` releases are infrequent and its bundled FIT profile lags Garmin's. New message types or fields may appear as unknown until it updates. If that becomes a real gap, the fallback is to regenerate its profile from Garmin's published profile, not to switch to the SDK.
