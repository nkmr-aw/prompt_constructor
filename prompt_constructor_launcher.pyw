# -*- coding: utf-8 -*-
import subprocess
import sys
import os


def get_pythonw_path():
    python_dir = os.path.dirname(sys.executable)
    pythonw_path = os.path.join(python_dir, 'pythonw.exe')
    return pythonw_path if os.path.exists(pythonw_path) else sys.executable


def run_py_script():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    py_script = "prompt_constructor.py"
    py_script_path = os.path.join(current_dir, py_script)

    pythonw_executable = get_pythonw_path()

    subprocess.Popen([pythonw_executable, py_script_path],
                     creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    run_py_script()

