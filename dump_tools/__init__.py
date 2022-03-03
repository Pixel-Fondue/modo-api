# Python
import sys
import subprocess
from pathlib import Path


# Get local paths for the dump
resources = Path(__file__) / "resources"
config = resources / "modo_cl.cfg"
dump_cmd = resources / "dump.py"


def dump(version: str):
    """Triggers the dump process for the given modo version.

    Args:
        version (str): Version of modo to dump.

    Returns:
        (str): The Modo stdout.
    """
    version = version if version else "15.1v1"
    # Build OS specific paths
    if sys.platform == "win32":
        app_path = f"C:/Program Files/Foundry/Modo/{version}/modo_cl.exe"
        py_dir = f"C:/Program Files/Foundry/Modo/{version}/extra/Python/modules"
    else:
        app_path = f"/Applications/Modo{version}.app/Contents/MacOS/modo_cl"
        py_dir = f"/Applications/Modo{version}.app/Contents/Extras/Python/modules"

    modo_cl = subprocess.Popen(
        [app_path, "-config:{}".format(config)],
        env={},
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True)

    modo_cl.stdin.write("log.toConsole true\n")
    # Run the dump command
    modo_cl.stdin.write(f"@{{{dump_cmd}}} {{{resources}}} {{{py_dir}}}\n")
    # Quit Modo
    modo_cl.stdin.write("app.quit\n")
    # Report log
    return modo_cl.stdout.read()
