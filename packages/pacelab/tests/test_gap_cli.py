from pacelab.cli import app
from typer.testing import CliRunner


def test_summary_can_include_grade_adjusted_pace(tmp_path, steady_run_fit):
    path = tmp_path / "flat.fit"
    path.write_bytes(steady_run_fit)
    runner = CliRunner()
    default = runner.invoke(app, ["summary", str(path)])
    enabled = runner.invoke(app, ["summary", "--include-gap", str(path)])
    assert default.exit_code == 0
    assert "GAP" not in default.stdout
    assert enabled.exit_code == 0, enabled.output
    assert "GAP 5:33 /km" in enabled.stdout
