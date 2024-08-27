# Prompt Constructor (prompt_constructor)
[English](#english) | [Japanese(日本語)](#japanese)

## English

### Introduction
“Prompt Constructor” is a prompt building tool for AI chat. It works standalone. 
It is made with Python+Tkinter, and has only been tested on Windows, so available for Windows only.  

### Installation & How to run
Run 'prompt_constructor_launcher.pyw' after 'git clone' to an appropriate location.  
When you run 'prompt_constructor.py', you can start and use the application normally, but get an extra black screen.  
Running it via 'prompt_constructor_launcher.pyw' will suppress the black screen.  
If you rename 'prompt_constructor.py' to 'prompt_constructor.pyw' and run it directly, you can suppress the black screen as well.  
(In this case, the launcher will not be usable unless codes inside are modified, but this is not a problem because changing the extension of the main body will make it worthless.)  
Note that a black screen does not interfere with the operation of the application. It's just an eyesore.  

Python must be installed in your environment. The assumed version is Python 3.12.5 or higher.  
There are files and folders that are automatically created when you run the program for the first time.  

### Uninstallation
The registry is not used, and uninstallation is completed by deleting the entire folder.  
Before deleting, be sure to save all necessary files.  

### If you want to build
This application is intended to be built and used, however, it is not recommended to build it using PyInstaller or Nuitka,  
as it is likely to be mis-detected as a malware.  

### Notes
Please use in accordance with the [LICENSE](./LICENSE).  

Please use at your own risk whether you build and use it or not.  
Thank you for your cooperation.



## Japanese

### はじめに
"Prompt Constructor"はAIチャット用のプロンプト作成ツールです。スタンドアロンで動作します。  
Python+Tkinterで作られています。Windowsでしか動作確認していませんので、Windows用とさせてください。  

### インストールと実行方法
適当な場所に'git clone'してから'prompt_constructor_launcher.pyw'を実行します。  
'prompt_constructor.py'を実行しても普通に起動してアプリを使用できますが、余計な黒い画面が出てきます。
'prompt_constructor_launcher.pyw'経由で実行すると黒い画面を抑止することができます。  
また、'prompt_constructor.py'を'prompt_constructor.pyw'にリネームして直接実行すると、同様に黒い画面が抑止できます。  
(この場合ランチャーは中身を修正しないと使えなくなりますが、本体の拡張子を変えると利用価値はなくなりますので問題はありません)  
なお、黒い画面が出てもアプリの動作には支障はありません。目障りなだけです。  

実行環境にPythonがインストールされている必要があります。 想定バージョンはPython 3.12.5 以上です。  
初回実行時に自動作成されるファイルやフォルダがあります。  

### アンインストール
レジストリなどは使用していませんので、フォルダごと削除すればアンインストール完了です。  
削除前に必要なファイル等を事前退避するなりしておいてください。  

### ビルドしたい場合
本アプリはビルドして使うことも想定して作ってあるつもりですが、  
PyInstallerやNuitkaを用いてビルドするとマルウェアとして誤検知される可能性が高いのでおすすめしません。  
なるべくビルドせずにそのままお使いください。  

### 注意事項
[ライセンス](./LICENSE)に従ってご利用ください。  

ビルドしてお使いになる場合もそうでない場合も自己責任でお使いください。  
よろしくお願いします。  


