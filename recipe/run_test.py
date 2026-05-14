import os
import sys
import tempfile
from pathlib import Path

import rootutils


with tempfile.TemporaryDirectory() as tmpdir:
    root = Path(tmpdir).resolve()
    nested = root / "package" / "module"
    nested.mkdir(parents=True)
    marker = root / ".project-root"
    marker.write_text("", encoding="utf-8")
    (root / ".env").write_text("ROOTUTILS_TEST_VALUE=from_dotenv\n", encoding="utf-8")
    start_file = nested / "example.py"
    start_file.write_text("# package-test marker\n", encoding="utf-8")

    found = rootutils.find_root(start_file, indicator=".project-root")
    assert found == root

    old_cwd = Path.cwd()
    try:
        configured = rootutils.setup_root(
            start_file,
            indicator=".project-root",
            project_root_env_var=True,
            dotenv=True,
            pythonpath=True,
            cwd=True,
        )
        assert configured == root
        assert Path.cwd() == root
        assert os.environ["PROJECT_ROOT"] == str(root)
        assert os.environ["ROOTUTILS_TEST_VALUE"] == "from_dotenv"
        assert sys.path[0] == str(root)
    finally:
        os.chdir(old_cwd)
