import hashlib
from dataclasses import dataclass
from pathlib import Path

import polars as pl
from pacelab import load
from pacelab.metrics import summarize
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from pacelab_server.db import ActivityRow


@dataclass(frozen=True, slots=True)
class ImportResult:
    activity_id: int
    created: bool


class Store:
    def __init__(self, data_dir: Path, engine: Engine) -> None:
        self.engine = engine
        self.originals = data_dir / "originals"
        self.streams = data_dir / "streams"
        self.originals.mkdir(parents=True, exist_ok=True)
        self.streams.mkdir(parents=True, exist_ok=True)

    def import_file(self, filename: str, data: bytes) -> ImportResult:
        digest = hashlib.sha256(data).hexdigest()
        with Session(self.engine) as session:
            existing = session.scalar(select(ActivityRow.id).where(ActivityRow.sha256 == digest))
            if existing is not None:
                return ImportResult(existing, created=False)
            activity = load(data)
            summary = summarize(activity)
            row = ActivityRow(
                sha256=digest,
                filename=Path(filename).name[:255] or "upload",
                source_format=activity.source_format,
                sport=activity.sport.value,
                device=activity.device,
                start_time=activity.start_time,
                distance_m=summary.distance_m,
                elapsed_s=summary.elapsed_s,
                moving_s=summary.moving_s,
                pace_s_per_km=summary.pace_s_per_km,
                avg_heart_rate=summary.avg_heart_rate,
                max_heart_rate=summary.max_heart_rate,
                elevation_gain_m=summary.elevation_gain_m,
            )
            session.add(row)
            session.flush()
            (self.originals / digest).write_bytes(data)
            activity.records.write_parquet(self.streams / f"{digest}.parquet")
            session.commit()
            return ImportResult(row.id, created=True)

    def list(self) -> list[ActivityRow]:
        with Session(self.engine) as session:
            return list(
                session.scalars(select(ActivityRow).order_by(ActivityRow.start_time.desc()))
            )

    def get(self, activity_id: int) -> ActivityRow | None:
        with Session(self.engine) as session:
            return session.get(ActivityRow, activity_id)

    def records(self, row: ActivityRow) -> pl.DataFrame:
        return pl.read_parquet(self.streams / f"{row.sha256}.parquet")
