# Prompt Constructor (prompt_constructor)
[English](#english) | [Japanese(日本語)](#japanese)

## English

### Introduction
“Prompt Constructor” is a prompt building tool for AI chat. It works standalone. 
It is made with Python+Tkinter, and has only been tested on Windows, so available for Windows only.  

### Required for run
The following must be installed in your environment.
* Python 3.12.x or later
* Cerberus 1.3.5 or later (Required for v1.0.22 and later.)

### Installation & How to run
Run 'prompt_constructor_launcher.pyw' after 'git clone' to an appropriate location.  
When you run 'prompt_constructor.py', you can start and use the application normally, but get an extra black screen.  
Running it via 'prompt_constructor_launcher.pyw' will suppress the black screen.  
If you rename 'prompt_constructor.py' to 'prompt_constructor.pyw' and run it directly, you can suppress the black screen as well.  
Note that a black screen does not interfere with the operation of the application. It's just an eyesore.  
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
* Python 3.12.x以降
* Cerberus 1.3.5以降 (v1.0.22以降で必要。)

### インストールと実行方法
適当な場所に'git clone'してから'prompt_constructor_launcher.pyw'を実行します。  
'prompt_constructor.py'を実行しても普通に起動してアプリを使用できますが、余計な黒い画面が出てきます。
'prompt_constructor_launcher.pyw'経由で実行すると黒い画面を抑止することができます。   
なお、黒い画面が出てもアプリの動作には支障はありません。目障りなだけです。  
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


