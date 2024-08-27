# prompt_constructor
[English](#english) | [日本語](#日本語)

## English

### Introduction
“prompt_constructor” is a prompt building tool for AI chat. It works standalone.
It is made with Python+Tkinter, and has only been tested on Windows, so supported for Windows only.

### Installation
Run main.py after 'git clone' to an appropriate location. Python must be installed in your environment. 
The assumed version is Python 3.12.5 or higher.
Since there are files and folders that are automatically created when you run the program for the first time, 
it is recommended that you place main.py in a new folder that you have created.

### Uninstallation
The registry is not used, and uninstallation is completed by deleting the entire folder.
Before deleting, be sure to save all necessary files.

### If you want to build
I have made main.py with the assumption that it will be built and used,
However, it is not recommended to build it using PyInstaller or Nuitka, 
as it is likely to be mis-detected as a virus or malware.

### Notes
Please use in accordance with the [LICENSE](./LICENSE).



## 日本語

### はじめに
"prompt_constructor "はAIチャット用のプロンプト作成ツールです。スタンドアロンで動作します。
Python+Tkinterで作られています。Windowsでしか動作確認していませんので、Windows用とさせてください。

### インストール方法
適当な場所に'git clone'してからmain.pyを実行します。実行環境にPythonがインストールされている必要があります。
想定バージョンはPython 3.12.5 以上です。
初回実行時に自動作成されるファイルやフォルダがありますので、main.pyを置く場所はなにか新規で適当に作成したフォルダの中が良いでしょう。

### アンインストール方法
レジストリなどは使用していませんので、フォルダごと削除すればアンインストール完了です。
削除前にあらかじめ必要なファイル等を退避するなりしておいてください。

### ビルドしたい場合
main.pyはビルドして使うことに想定して作ってあるつもりですが、
PyInstallerやNuitkaを用いてビルドするとウイルスやマルウェアとして誤検知される可能性が高いのでおすすめしません。

### 注意事項
[ライセンス](./LICENSE)に従ってご利用ください。