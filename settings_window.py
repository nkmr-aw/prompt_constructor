# -*- coding: utf-8 -*-
import os
import sys
import configparser
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox
from check_settings import validate_settings, sanitize_input


# 設定ファイルのパス
settings_path = os.path.join(os.path.dirname(sys.argv[0]), 'settings.ini')


class settings(tk.Toplevel):
    def __init__(self, parent):  # parent 引数を追加
        super().__init__(parent.root)
        self.parent = parent  # メインウィンドウへの参照を保持

        # 設定値の読み込み
        config = configparser.ConfigParser()
        config.read(settings_path)

        # 設定画面のウィンドウを作成
        # 新しいウィンドウ(Toplevel)が作成されると、
        # attributes("-topmost", True)で最上位に表示される
        # grab_set()で元のウィンドウが一時的に無効化される
        #settings_window = tk.Toplevel(parent.root)
        self.title("Settings")
        self.attributes("-topmost", True)
        self.grab_set()  # このウインドウを閉じる処理の中で destroy() の前に grab_release() を実施


        # 設定項目のフレーム
        settings_frame = tk.Frame(self)
        settings_frame.pack(padx=10, pady=10, anchor='w')


        # 言語設定
        lang_frame = tk.Frame(settings_frame)
        lang_frame.pack(pady=5, anchor='w')
        self.lang_var = tk.StringVar(value=config['Settings']['lang'])
        label = tk.Label(lang_frame, text="lang: ")
        label.pack(side=tk.LEFT)
        en_radio = tk.Radiobutton(lang_frame, text="en", variable=self.lang_var, value="en")
        en_radio.pack(side=tk.LEFT)
        ja_radio = tk.Radiobutton(lang_frame, text="ja", variable=self.lang_var, value="ja")
        ja_radio.pack(side=tk.LEFT)


        # インクリメント単位設定
        increment_unit_frame = tk.Frame(settings_frame)
        increment_unit_frame.pack(pady=5, anchor='w')
        self.increment_unit_var = tk.StringVar(value=config['Settings']['increment_unit'])
        label = tk.Label(increment_unit_frame, text="increment_unit: ")
        label.pack(side=tk.LEFT)
        unit_radio = tk.Radiobutton(increment_unit_frame, text="0.05", variable=self.increment_unit_var, value="0.05")
        unit_radio.pack(side=tk.LEFT)
        unit01_radio = tk.Radiobutton(increment_unit_frame, text="0.1", variable=self.increment_unit_var, value="0.1")
        unit01_radio.pack(side=tk.LEFT)


        # ウィンドウ幅設定
        window_width_frame = tk.Frame(settings_frame)
        window_width_frame.pack(pady=5, anchor='w')
        label = tk.Label(window_width_frame, text="window_width: ")
        label.pack(side=tk.LEFT)
        self.window_width_entry = tk.Entry(window_width_frame)
        self.window_width_entry.insert(0, config['Settings']['window_width'])
        self.window_width_entry.pack(side=tk.LEFT)


        # ウィンドウ高さ設定
        window_height_frame = tk.Frame(settings_frame)
        window_height_frame.pack(pady=5, anchor='w')
        label = tk.Label(window_height_frame, text="window_height: ")
        label.pack(side=tk.LEFT)
        self.window_height_entry = tk.Entry(window_height_frame)
        self.window_height_entry.insert(0, config['Settings']['window_height'])
        self.window_height_entry.pack(side=tk.LEFT)


        # 左ペイン幅設定
        left_pane_width_frame = tk.Frame(settings_frame)
        left_pane_width_frame.pack(pady=5, anchor='w')
        label = tk.Label(left_pane_width_frame, text="left_pane_width: ")
        label.pack(side=tk.LEFT)
        self.left_pane_width_entry = tk.Entry(left_pane_width_frame)
        self.left_pane_width_entry.insert(0, config['Settings']['left_pane_width'])
        self.left_pane_width_entry.pack(side=tk.LEFT)


        # アイテム欄の表示行数設定
        itemarea_displines_frame = tk.Frame(settings_frame)
        itemarea_displines_frame.pack(pady=5, anchor='w')
        label = tk.Label(itemarea_displines_frame, text="itemarea_displines: ")
        label.pack(side=tk.LEFT)
        self.itemarea_displines_entry = tk.Entry(itemarea_displines_frame)
        self.itemarea_displines_entry.insert(0, config['Settings']['itemarea_displines'])
        self.itemarea_displines_entry.pack(side=tk.LEFT)


        # マウスホイールによるスクロール行数設定
        scroll_lines_frame = tk.Frame(settings_frame)
        scroll_lines_frame.pack(pady=5, anchor='w')
        label = tk.Label(scroll_lines_frame, text="scroll_lines: ")
        label.pack(side=tk.LEFT)
        self.scroll_lines_entry = tk.Entry(scroll_lines_frame)
        self.scroll_lines_entry.insert(0, config['Settings']['scroll_lines'])
        self.scroll_lines_entry.pack(side=tk.LEFT)


        # メッセージ表示設定
        messages_frame = tk.Frame(settings_frame)
        messages_frame.pack(pady=5, anchor='w')
        messages_var = tk.StringVar(value=config['Settings']['messages'])
        label = tk.Label(messages_frame, text="messages: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(messages_frame, text="enable", variable=messages_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(messages_frame, text="disable", variable=messages_var, value="disable")
        disable_radio.pack(side=tk.LEFT)


        # 自動保存設定
        autosave_json_frame = tk.Frame(settings_frame)
        autosave_json_frame.pack(pady=5, anchor='w')
        autosave_json_var = tk.StringVar(value=config['Settings']['autosave_json'])
        label = tk.Label(autosave_json_frame, text="autosave_json: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(autosave_json_frame, text="enable", variable=autosave_json_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(autosave_json_frame, text="disable", variable=autosave_json_var, value="disable")
        disable_radio.pack(side=tk.LEFT)


        # バックアップ設定
        backup_json_frame = tk.Frame(settings_frame)
        backup_json_frame.pack(pady=5, anchor='w')
        backup_json_var = tk.StringVar(value=config['Settings']['backup_json'])
        label = tk.Label(backup_json_frame, text="backup_json: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(backup_json_frame, text="enable", variable=backup_json_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(backup_json_frame, text="disable", variable=backup_json_var, value="disable")
        disable_radio.pack(side=tk.LEFT)

        # システムにインストールされているフォント名一覧を取得+TkDefaultFont
        self.available_fonts = ["TkDefaultFont"]
        self.available_fonts += tkFont.families()

        # 表示フォント設定
        textfont_frame = tk.Frame(settings_frame)
        textfont_frame.pack(pady=5, anchor='w')
        label = tk.Label(textfont_frame, text="textfont: ")
        label.pack(side=tk.LEFT)
        self.textfont_var = tk.StringVar(value=config['Settings']['textfont'])
        self.textfont_combobox = ttk.Combobox(
            textfont_frame,
            textvariable=self.textfont_var,
            values=self.available_fonts,
            state="readonly"  # 直接入力を禁止
        )
        self.textfont_combobox.pack(side=tk.LEFT)


        # ツリー表示のフォントサイズ設定
        fontsize_treeview_frame = tk.Frame(settings_frame)
        fontsize_treeview_frame.pack(pady=5, anchor='w')
        label = tk.Label(fontsize_treeview_frame, text="fontsize_treeview: ")
        label.pack(side=tk.LEFT)
        self.fontsize_treeview_entry = tk.Entry(fontsize_treeview_frame)
        self.fontsize_treeview_entry.insert(0, config['Settings']['fontsize_treeview'])
        self.fontsize_treeview_entry.pack(side=tk.LEFT)


        # テキストボックス表示のフォントサイズ設定
        fontsize_textbox_frame = tk.Frame(settings_frame)
        fontsize_textbox_frame.pack(pady=5, anchor='w')
        label = tk.Label(fontsize_textbox_frame, text="fontsize_textbox: ")
        label.pack(side=tk.LEFT)
        self.fontsize_textbox_entry = tk.Entry(fontsize_textbox_frame)
        self.fontsize_textbox_entry.insert(0, config['Settings']['fontsize_textbox'])
        self.fontsize_textbox_entry.pack(side=tk.LEFT)


        # 日時フォーマット設定
        datetime_format_frame = tk.Frame(settings_frame)
        datetime_format_frame.pack(pady=5, anchor='w')
        label = tk.Label(datetime_format_frame, text="datetime_format: ")
        label.pack(side=tk.LEFT)
        self.datetime_format_entry = tk.Entry(datetime_format_frame)
        self.datetime_format_entry.insert(0, config['Settings']['datetime_format'])
        self.datetime_format_entry.pack(side=tk.LEFT)


        # 多重起動設定
        multiple_boot_frame = tk.Frame(settings_frame)
        multiple_boot_frame.pack(pady=5, anchor='w')
        multiple_boot_var = tk.StringVar(value=config['Settings']['multiple_boot'])
        label = tk.Label(multiple_boot_frame, text="multiple_boot: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(multiple_boot_frame, text="enable", variable=multiple_boot_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(multiple_boot_frame, text="disable", variable=multiple_boot_var, value="disable")
        disable_radio.pack(side=tk.LEFT)




        # デフォルトボタン
        def set_default():
            self.lang_var.set("en")
            self.increment_unit_var.set("0.05")
            messages_var.set("enable")
            autosave_json_var.set("disable")
            backup_json_var.set("enable")
            multiple_boot_var.set("disable")
            self.window_width_entry.delete(0, tk.END)
            self.window_width_entry.insert(0, "1000")
            self.window_height_entry.delete(0, tk.END)
            self.window_height_entry.insert(0, "600")
            self.left_pane_width_entry.delete(0, tk.END)
            self.left_pane_width_entry.insert(0, "300")
            self.itemarea_displines_entry.delete(0, tk.END)
            self.itemarea_displines_entry.insert(0, "5")
            self.scroll_lines_entry.delete(0, tk.END)
            self.scroll_lines_entry.insert(0, "3")
            self.textfont_combobox.set("TkDefaultFont")
            self.fontsize_treeview_entry.delete(0, tk.END)
            self.fontsize_treeview_entry.insert(0, "12")
            self.fontsize_textbox_entry.delete(0, tk.END)
            self.fontsize_textbox_entry.insert(0, "12")
            self.datetime_format_entry.delete(0, tk.END)
            self.datetime_format_entry.insert(0, "%Y%m%d_%H%M%S")

        # 適用ボタン
        def apply_settings():
            try:
                settings = {
                    'lang': self.lang_var.get(),
                    'increment_unit': float(self.increment_unit_var.get()),
                    'window_width': int(self.window_width_entry.get()),
                    'window_height': int(self.window_height_entry.get()),
                    'left_pane_width': int(self.left_pane_width_entry.get()),
                    'itemarea_displines': int(self.itemarea_displines_entry.get()),
                    'scroll_lines': int(self.scroll_lines_entry.get()),
                    'messages': messages_var.get(),
                    'autosave_json': autosave_json_var.get(),
                    'backup_json': backup_json_var.get(),
                    'textfont': self.textfont_combobox.get(),
                    'fontsize_treeview': int(self.fontsize_treeview_entry.get()),
                    'fontsize_textbox': int(self.fontsize_textbox_entry.get()),
                    'datetime_format': self.datetime_format_entry.get().replace('%', '%%'),
                    'multiple_boot': multiple_boot_var.get(),
                }

                is_valid, errors = validate_settings(settings)
                if not is_valid:
                    error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
                    messagebox.showerror("Configuration Error", error_message)
                    return

                # サニタイズと設定ファイルへの保存
                config = configparser.ConfigParser()
                config['Settings'] = {}
                for key, value in settings.items():
                    config['Settings'][key] = str(sanitize_input(value, type(value).__name__))

                with open(settings_path, 'w') as configfile:
                    config.write(configfile)

                    # iniファイルのクリンナップ
                    cleanup_ini_file(settings_path)

                    # 親ウインドウ側の変数更新とメソッド呼び出しによる、
                    # 「辞書オートセーブ」チェックボックスへのiniファイル設定の反映
                    self.parent.autosave_json_enabled = config['Settings'].get('autosave_json', 'enable') == 'enable'
                    self.parent.autosave_json_var = tk.BooleanVar(value=self.parent.autosave_json_enabled)
                    self.parent.autosave_json_checkbox.config(variable=self.parent.autosave_json_var)
                    self.parent.toggle_autosave_json()

                    lang = self.lang_var.get()
                    if lang == 'en':
                        messagebox.showinfo("Settings","Settings saved successfully.\nRestart the application to apply the changes.")
                    elif lang == 'ja':
                        messagebox.showinfo("設定", "設定を保存しました。\n設定を反映するにはアプリを再起動してください。")

            except Exception as e:
                messagebox.showerror("Configuration Error", str(e))
                return


        def close_window():
            self.grab_release()
            # 設定画面を閉じる
            self.destroy()


        # ボタンフレーム
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # 「デフォルト」ボタン
        default_button = tk.Button(button_frame, text="Default", width=8, command=set_default)
        default_button.pack(side=tk.LEFT, padx=10)

        # 「適用」ボタン
        apply_button = tk.Button(button_frame, text="Apply", width=8, command=apply_settings)
        apply_button.pack(side=tk.LEFT, padx=10)

        # 「キャンセル」ボタン
        cancel_button = tk.Button(button_frame, text="Cancel", width=8, command=close_window)
        cancel_button.pack(side=tk.LEFT, padx=10)

        # 「閉じる」ボタン
        close_button = tk.Button(button_frame, text="Close", width=8, command=close_window)
        close_button.pack(side=tk.LEFT, padx=10)


        # 設定画面を表示
        self.mainloop()

        # コンストラクタは None を返す必要がある
        return None


def cleanup_ini_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 有効な設定行とセクション見出しのみを保持
    valid_lines = []
    for line in lines:
        line = line.strip()
        if line and (line.startswith('[') or '=' in line):
            valid_lines.append(line + '\n')

    # クリーンアップされた内容を書き込む
    with open(file_path, 'w') as file:
        file.writelines(valid_lines)



