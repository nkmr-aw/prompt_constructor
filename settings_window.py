import tkinter as tk
from tkinter import ttk, messagebox, Menu
import tkinter.font as tkFont
import configparser
import os
import sys


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
        settings_frame.pack(padx=10, pady=10)


        # 言語設定
        lang_frame = tk.LabelFrame(settings_frame, text="")
        lang_frame.pack(pady=5)
        lang_var = tk.StringVar(value=config['Settings']['lang'])
        label = tk.Label(lang_frame, text="lang: ")
        label.pack(side=tk.LEFT)
        en_radio = tk.Radiobutton(lang_frame, text="en", variable=lang_var, value="en")
        en_radio.pack(side=tk.LEFT)
        ja_radio = tk.Radiobutton(lang_frame, text="ja", variable=lang_var, value="ja")
        ja_radio.pack(side=tk.LEFT)


        # インクリメント単位設定
        increment_unit_frame = tk.LabelFrame(settings_frame, text="")
        increment_unit_frame.pack(pady=5)
        increment_unit_var = tk.StringVar(value=config['Settings']['increment_unit'])
        label = tk.Label(increment_unit_frame, text="increment_unit: ")
        label.pack(side=tk.LEFT)
        unit_radio = tk.Radiobutton(increment_unit_frame, text="0.05", variable=increment_unit_var, value="0.05")
        unit_radio.pack(side=tk.LEFT)
        unit01_radio = tk.Radiobutton(increment_unit_frame, text="0.1", variable=increment_unit_var, value="0.1")
        unit01_radio.pack(side=tk.LEFT)


        # ウィンドウ幅設定
        window_width_frame = tk.LabelFrame(settings_frame, text="")
        window_width_frame.pack(pady=5)
        label = tk.Label(window_width_frame, text="window_width: ")
        label.pack(side=tk.LEFT)
        window_width_entry = tk.Entry(window_width_frame)
        window_width_entry.insert(0, config['Settings']['window_width'])
        window_width_entry.pack(side=tk.LEFT)


        # ウィンドウ高さ設定
        window_height_frame = tk.LabelFrame(settings_frame, text="")
        window_height_frame.pack(pady=5)
        label = tk.Label(window_height_frame, text="window_height: ")
        label.pack(side=tk.LEFT)
        window_height_entry = tk.Entry(window_height_frame)
        window_height_entry.insert(0, config['Settings']['window_height'])
        window_height_entry.pack(side=tk.LEFT)


        # アイテム欄の表示行数設定
        itemarea_displines_frame = tk.LabelFrame(settings_frame, text="")
        itemarea_displines_frame.pack(pady=5)
        label = tk.Label(itemarea_displines_frame, text="itemarea_displines: ")
        label.pack(side=tk.LEFT)
        itemarea_displines_entry = tk.Entry(itemarea_displines_frame)
        itemarea_displines_entry.insert(0, config['Settings']['itemarea_displines'])
        itemarea_displines_entry.pack(side=tk.LEFT)


        # メッセージ表示設定
        messages_frame = tk.LabelFrame(settings_frame, text="")
        messages_frame.pack(pady=5)
        messages_var = tk.StringVar(value=config['Settings']['messages'])
        label = tk.Label(messages_frame, text="messages: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(messages_frame, text="enable", variable=messages_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(messages_frame, text="disable", variable=messages_var, value="disable")
        disable_radio.pack(side=tk.LEFT)


        # 自動保存設定
        autosave_json_frame = tk.LabelFrame(settings_frame, text="")
        autosave_json_frame.pack(pady=5)
        autosave_json_var = tk.StringVar(value=config['Settings']['autosave_json'])
        label = tk.Label(autosave_json_frame, text="autosave_json: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(autosave_json_frame, text="enable", variable=autosave_json_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(autosave_json_frame, text="disable", variable=autosave_json_var, value="disable")
        disable_radio.pack(side=tk.LEFT)


        # バックアップ設定
        backup_json_frame = tk.LabelFrame(settings_frame, text="")
        backup_json_frame.pack(pady=5)
        backup_json_var = tk.StringVar(value=config['Settings']['backup_json'])
        label = tk.Label(backup_json_frame, text="backup_json: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(backup_json_frame, text="enable", variable=backup_json_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(backup_json_frame, text="disable", variable=backup_json_var, value="disable")
        disable_radio.pack(side=tk.LEFT)


        # 表示フォント設定
        textfont_frame = tk.LabelFrame(settings_frame, text="")
        textfont_frame.pack(pady=5)
        label = tk.Label(textfont_frame, text="textfont: ")
        label.pack(side=tk.LEFT)
        textfont_entry = tk.Entry(textfont_frame)
        textfont_entry.insert(0, config['Settings']['textfont'])
        textfont_entry.pack(side=tk.LEFT)


        # ツリー表示のフォントサイズ設定
        fontsize_treeview_frame = tk.LabelFrame(settings_frame, text="")
        fontsize_treeview_frame.pack(pady=5)
        label = tk.Label(fontsize_treeview_frame, text="fontsize_treeview: ")
        label.pack(side=tk.LEFT)
        fontsize_treeview_entry = tk.Entry(fontsize_treeview_frame)
        fontsize_treeview_entry.insert(0, config['Settings']['fontsize_treeview'])
        fontsize_treeview_entry.pack(side=tk.LEFT)


        # テキストボックス表示のフォントサイズ設定
        fontsize_textbox_frame = tk.LabelFrame(settings_frame, text="")
        fontsize_textbox_frame.pack(pady=5)
        label = tk.Label(fontsize_textbox_frame, text="fontsize_textbox: ")
        label.pack(side=tk.LEFT)
        fontsize_textbox_entry = tk.Entry(fontsize_textbox_frame)
        fontsize_textbox_entry.insert(0, config['Settings']['fontsize_textbox'])
        fontsize_textbox_entry.pack(side=tk.LEFT)


        # 日時フォーマット設定
        datetime_format_frame = tk.LabelFrame(settings_frame, text="")
        datetime_format_frame.pack(pady=5)
        label = tk.Label(datetime_format_frame, text="datetime_format: ")
        label.pack(side=tk.LEFT)
        datetime_format_entry = tk.Entry(datetime_format_frame)
        datetime_format_entry.insert(0, config['Settings']['datetime_format'])
        datetime_format_entry.pack(side=tk.LEFT)


        # 多重起動設定
        multiple_boot_frame = tk.LabelFrame(settings_frame, text="")
        multiple_boot_frame.pack(pady=5)
        multiple_boot_var = tk.StringVar(value=config['Settings']['multiple_boot'])
        label = tk.Label(multiple_boot_frame, text="multiple_boot: ")
        label.pack(side=tk.LEFT)
        enable_radio = tk.Radiobutton(multiple_boot_frame, text="enable", variable=multiple_boot_var, value="enable")
        enable_radio.pack(side=tk.LEFT)
        disable_radio = tk.Radiobutton(multiple_boot_frame, text="disable", variable=multiple_boot_var, value="disable")
        disable_radio.pack(side=tk.LEFT)


        # デフォルトボタン
        def set_default():
            lang_var.set("en")
            increment_unit_var.set("0.05")
            messages_var.set("enable")
            autosave_json_var.set("disable")
            backup_json_var.set("enable")
            multiple_boot_var.set("disable")
            window_width_entry.delete(0, tk.END)
            window_width_entry.insert(0, "1000")
            window_height_entry.delete(0, tk.END)
            window_height_entry.insert(0, "600")
            itemarea_displines_entry.delete(0, tk.END)
            itemarea_displines_entry.insert(0, "5")
            textfont_entry.delete(0, tk.END)
            textfont_entry.insert(0, "TkDefaultFont")
            fontsize_treeview_entry.delete(0, tk.END)
            fontsize_treeview_entry.insert(0, "12")
            fontsize_textbox_entry.delete(0, tk.END)
            fontsize_textbox_entry.insert(0, "12")
            datetime_format_entry.delete(0, tk.END)
            datetime_format_entry.insert(0, "%Y%m%d_%H%M%S")

        # 適用ボタン
        def apply_settings():
            config['Settings']['lang'] = lang_var.get()
            config['Settings']['increment_unit'] = increment_unit_var.get()
            config['Settings']['messages'] = messages_var.get()
            config['Settings']['autosave_json'] = autosave_json_var.get()
            config['Settings']['backup_json'] = backup_json_var.get()
            config['Settings']['multiple_boot'] = multiple_boot_var.get()
            config['Settings']['window_width'] = window_width_entry.get()
            config['Settings']['window_height'] = window_height_entry.get()
            config['Settings']['itemarea_displines'] = itemarea_displines_entry.get()
            config['Settings']['textfont'] = textfont_entry.get()
            config['Settings']['fontsize_treeview'] = fontsize_treeview_entry.get()
            config['Settings']['fontsize_textbox'] = fontsize_textbox_entry.get()
            # config['Settings']['datetime_format'] = datetime_format_entry.get()
            config['Settings']['datetime_format'] = datetime_format_entry.get().replace('%', '%%')

            # 設定値のバリデーション

            fontsize_min = 8
            fontsize_max = 32
            fontsize_treeview = int((config['Settings'].get('fontsize_treeview', '12')))
            fontsize_textbox = int((config['Settings'].get('fontsize_textbox', '12')))
            itemarea_displines_min = 1
            itemarea_displines_max = 20
            itemarea_displines = int(config['Settings'].get('itemarea_displines', '5'))

            if not (fontsize_min <= fontsize_treeview <= fontsize_max):
                messagebox.showerror("Configuration Error", f"Invalid value set for 'fontsize_treeview' \nIt must be between {fontsize_min} and {fontsize_max}.")

            elif not (fontsize_min <= fontsize_textbox <= fontsize_max):
                messagebox.showerror("Configuration Error", f"Invalid value set for 'fontsize_textbox' \nIt must be between {fontsize_min} and {fontsize_max}.")

            elif not (itemarea_displines_min <= itemarea_displines <= itemarea_displines_max):
                messagebox.showerror("Configuration Error", f"Invalid value set for 'itemarea_displines'. \nIt must be between {itemarea_displines_min} and {itemarea_displines_max}.")

            else:  # バリデーションがすべて通ったときのみ実施する
                with open(settings_path, 'w') as configfile:
                    config.write(configfile)

                    # 親ウインドウ側の変数更新とメソッド呼び出しによる、
                    # 「辞書オートセーブ」チェックボックスへのiniファイル設定の反映
                    self.parent.autosave_json_enabled = config['Settings'].get('autosave_json', 'enable') == 'enable'
                    self.parent.autosave_json_var = tk.BooleanVar(value=self.parent.autosave_json_enabled)
                    self.parent.autosave_json_checkbox.config(variable=self.parent.autosave_json_var)
                    self.parent.toggle_autosave_json()

                    lang = lang_var.get()
                    if lang == 'en':
                        messagebox.showinfo("Settings","Settings saved successfully.\nRestart the application to apply the changes.")
                    elif lang == 'ja':
                        messagebox.showinfo("設定", "設定を保存しました。\n設定を反映するにはアプリを再起動してください。")


        def close_window():
            self.grab_release()
            # 設定画面を閉じる
            self.destroy()


        # ボタンフレーム
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # 「デフォルト」ボタン
        default_button = tk.Button(button_frame, text="Default", command=set_default)
        default_button.pack(side=tk.LEFT)

        # 「適用」ボタン
        apply_button = tk.Button(button_frame, text="Apply", command=apply_settings)
        apply_button.pack(side=tk.LEFT)

        # 「キャンセル」ボタン
        cancel_button = tk.Button(button_frame, text="Cancel", command=close_window)
        cancel_button.pack(side=tk.LEFT)

        # 「閉じる」ボタン
        close_button = tk.Button(button_frame, text="Close", command=close_window)
        close_button.pack(side=tk.LEFT)


        # 設定画面を表示
        self.mainloop()

        # コンストラクタは None を返す必要がある
        return None



