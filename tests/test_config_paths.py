"""Keep path overrides isolated from the user's real configuration."""

import os
import subprocess
import sys


def test_overrides_redirect_session_edits_and_preferences(tmp_path):
    sessions = tmp_path / "sessions.toml"
    preferences = tmp_path / "preferences" / "config.toml"
    sessions.write_text('[[session]]\nname = "dotfiles"\npath = "~/dotfiles"\n')
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            """
import os
from unittest.mock import patch
from click.testing import CliRunner
from seshy.cli import cli
from seshy.config import CONFIG_PATH, get_default_icon
from seshy.toml_ops import SESH_TOML_PATH, add_session, delete_session, list_sessions
assert str(SESH_TOML_PATH) == os.environ['SESH_CONFIG_PATH']
assert str(CONFIG_PATH) == os.environ['SESHY_CONFIG_PATH']
assert list_sessions() == ['dotfiles']
assert get_default_icon() == '💻'
assert CONFIG_PATH.exists()
add_session('temporary', '~/code/tools/temporary', '🔧', 51)
assert list_sessions() == ['dotfiles', '51 temporary 🔧']
assert delete_session('51 temporary 🔧')
assert list_sessions() == ['dotfiles']
runner = CliRunner()
assert runner.invoke(cli, ['list']).output.strip() == 'dotfiles'
with patch('seshy.cli.os.execvp') as editor:
    assert runner.invoke(cli, ['read']).exit_code == 0
    editor.assert_called_once_with('nvim', ['nvim', str(SESH_TOML_PATH)])
with patch('seshy.cli.fzf_select', return_value='dotfiles'):
    with patch('seshy.cli.os.execvp') as editor:
        assert runner.invoke(cli, ['update']).exit_code == 0
        editor.assert_called_once_with('nvim', ['nvim', '+1', str(SESH_TOML_PATH)])
CONFIG_PATH.write_text('[groups]\\nwork = ["dotfiles"]\\n')
with patch('seshy.workflows.startup.subprocess.run') as launch:
    assert runner.invoke(cli, ['startup', 'work']).exit_code == 0
    launch.assert_called_once_with(
        ['sesh', 'connect', 'dotfiles'], check=True, capture_output=True
    )
""",
        ],
        env=dict(
            os.environ,
            SESH_CONFIG_PATH=str(sessions),
            SESHY_CONFIG_PATH=str(preferences),
        ),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_default_paths_and_tilde_expansion(tmp_path):
    script = """
from pathlib import Path
from seshy.config import CONFIG_PATH
from seshy.toml_ops import SESH_TOML_PATH
assert SESH_TOML_PATH == Path.home() / '.config/sesh/sesh.toml'
assert CONFIG_PATH == Path.home() / '.config/seshy/config.toml'
"""
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"SESH_CONFIG_PATH", "SESHY_CONFIG_PATH"}
    }
    subprocess.run([sys.executable, "-c", script], env=env, check=True)
    script = """
from pathlib import Path
from seshy.config import CONFIG_PATH
from seshy.toml_ops import SESH_TOML_PATH
assert SESH_TOML_PATH == Path.home() / 'sessions.toml'
assert CONFIG_PATH == Path.home() / 'preferences.toml'
"""
    env.update(
        SESH_CONFIG_PATH="~/sessions.toml", SESHY_CONFIG_PATH="~/preferences.toml"
    )
    subprocess.run([sys.executable, "-c", script], env=env, check=True)
