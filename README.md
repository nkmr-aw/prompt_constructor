# Prompt Constructor (prompt_constructor)
[English](#english) | [Japanese(日本語)](#japanese)

## English

### Introduction
“Prompt Constructor” is a prompt building tool for AI chat. It works standalone. 
It is made with Python+Tkinter, and has only been tested on Windows, so available for Windows only.  

### Required for run
The following must be installed in your environment.
* Python 3.12 or later
* [uv](https://github.com/astral-sh/uv) (Recommended) or pip

### Installation & How to run
Clone the repository to an appropriate location.

#### Using uv (Recommended)
1. Run `uv sync` in the project directory to set up the environment.
2. Run `prompt_constructor_launcher.pyw`.

#### Using pip
1. Run `pip install -r requirements.txt` to install dependencies.
2. Run `prompt_constructor_launcher.pyw`.

When you run 'prompt_constructor.py', you can start and use the application normally, but get an extra black screen.  
Running it via 'prompt_constructor_launcher.pyw' will suppress the black screen.
Please note that the black screen is merely an eyesore and does not affect the operation of the app.

There are files and folders that are automatically created when you run the program for the first time. 
Works entirely locally.  

### Uninstallation
The registry is not used, and uninstallation is completed by deleting the entire folder.  
Before deleting, be sure to save all necessary files.  

### Manual
[HERE.](https://sites.google.com/view/nkmr-appworks/apps/pcon_en)

### If you want to build
This application is intended to be built and used, however, it is not recommended to build it using PyInstaller or Nuitka,  
as it is likely to be mis-detected as a malware.  
Please use the application as is without building it as much as possible.  

### Notes
Please use in accordance with the [LICENSE](./LICENSE).  

Please use at your own risk whether you build and use it or not.  
Thank you for your cooperation.



## Japanese

### はじめに
"Prompt Constructor"はAIチャット用のプロンプト作成ツールです。スタンドアロンで動作します。  
Python+Tkinterで作られています。Windowsでしか動作確認していませんので、Windows用とさせてください。  

### 必要なもの
実行環境に以下のものがインストールされている必要があります。
* Python 3.12以降
* [uv](https://github.com/astral-sh/uv) (推奨) または pip

### インストールと実行方法
適当な場所にリポジトリをクローンしてください。

#### uv を使う場合 (推奨)
1. プロジェクトフォルダで `uv sync` を実行して環境をセットアップします。
2. `prompt_constructor_launcher.pyw` を実行します。

#### pip を使う場合
1. `pip install -r requirements.txt` を実行して依存関係をインストールします。
2. `prompt_constructor_launcher.pyw` を実行します。

'prompt_constructor.py'を実行しても普通に起動してアプリを使用できますが、余計な黒い画面が出てきます。
'prompt_constructor_launcher.pyw'経由で実行すると黒い画面を抑止することができます。   
なお、黒い画面が出ても目障りなだけでアプリの動作には支障はありません。 

初回実行時に自動作成されるファイルやフォルダがあります。
完全にローカルで実行できます。

### アンインストール
レジストリなどは使用していませんので、フォルダごと削除すればアンインストール完了です。  
削除前に必要なファイル等を事前退避するなりしておいてください。  

### マニュアル
[ココです。](https://sites.google.com/view/nkmr-appworks/apps/pcon_ja)

### ビルドしたい場合
本アプリはビルドして使うことも想定して作ってあるつもりですが、  
PyInstallerやNuitkaを用いてビルドするとマルウェアとして誤検知される可能性が高いのでおすすめしません。  
なるべくビルドせずにそのままお使いください。  

### 注意事項
[ライセンス](./LICENSE)に従ってご利用ください。  

ビルドしてお使いになる場合もそうでない場合も自己責任でお使いください。  
よろしくお願いします。  
