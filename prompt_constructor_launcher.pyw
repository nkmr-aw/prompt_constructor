# -*- coding: utf-8 -*-
import subprocess
import sys
import os


def get_python_executable():
    """
    実行に使用するPythonインタプリタのパスを取得する。
    1. プロジェクト内の .venv (uv作成の仮想環境) を優先
    2. なければ現在の実行環境と同じ場所にある pythonw.exe
    3. それもなければ現在の sys.executable
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. .venv 内の pythonw.exe をチェック
    venv_pythonw = os.path.join(current_dir, ".venv", "Scripts", "pythonw.exe")
    if os.path.exists(venv_pythonw):
        return venv_pythonw

    # 2. 現在のPython環境の pythonw.exe をチェック
    python_dir = os.path.dirname(sys.executable)
    sys_pythonw = os.path.join(python_dir, 'pythonw.exe')
    if os.path.exists(sys_pythonw):
        return sys_pythonw

    # 3. フォールバック
    return sys.executable


def run_py_script():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    py_script = "prompt_constructor.py"
    py_script_path = os.path.join(current_dir, py_script)

    python_executable = get_python_executable()

    # 仮想環境経由でない場合、依存ライブラリが見つからない可能性があるが、
    # その場合はユーザー側の環境構築不備となる。
    subprocess.Popen([python_executable, py_script_path],
                     creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    run_py_script()
