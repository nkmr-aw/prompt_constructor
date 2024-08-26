import os
import sys
import json
import configparser
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from glob import glob
import re
import random


version = "1.0.0"

# 言語設定の読み込み
config = configparser.ConfigParser()
settings_path = os.path.join(os.path.dirname(sys.argv[0]), 'settings.ini')
if not os.path.exists(settings_path):
    config['Settings'] = {
        'lang': 'en', 
        'increment_unit': '0.05', 
        'window_width': '1000',  # 初期ウィンドウ幅
        'window_height': '600',   # 初期ウィンドウ高さ
        'messages': 'enable',  # メッセージの表示(enable)と抑止(disable)
        'autosave_json': 'disable',  # JSON辞書ファイルの自動保存設定
        'backup_json': 'enable',  # アプリ起動時にJSON辞書ファイルを自動バックアップする設定
        'textfont': 'TkDefaultFont',
        'fontsize_treeview': '12',
        'fontsize_textbox': '12',
        'datetime_format': '%%Y%%m%%d_%%H%%M%%S',
        }
    with open(settings_path, 'w') as configfile:
        config.write(configfile)
else:
    config.read(settings_path)

# 設定値のバリデーション
lang = config['Settings']['lang']
if lang not in ['en', 'ja']:
    messagebox.showerror("Configuration Error", "Invalid value set for 'lang'. \nIt must be 'en' or 'ja'.")
    sys.exit(1)  # Exit the program

increment_unit = float(config['Settings'].get('increment_unit', '0.1'))
if increment_unit not in [0.05, 0.1]:
    messagebox.showerror("Configuration Error", "Invalid value set for 'increment_unit'. \nIt must be 0.05 or 0.1.")
    sys.exit(1)  # Exit the program

# textfontのチェックはstartメソッドで実施(理由もそちらに記載)
textfont = config['Settings']['textfont']

fontsize_textbox = int((config['Settings'].get('fontsize_textbox', '12')))
if not 8 <= fontsize_textbox <= 96:
    messagebox.showerror("Configuration Error", "Invalid value set for 'fontsize_textbox' \nIt must be between 8 and 32.")
    sys.exit(1)  # Exit the program

fontsize_treeview = int((config['Settings'].get('fontsize_treeview', '12')))
if not 8 <= fontsize_textbox <= 96:
    messagebox.showerror("Configuration Error", "Invalid value set for 'fontsize_treeview' \nIt must be between 8 and 32.")
    sys.exit(1)  # Exit the program


# ウィンドウサイズの取得
window_width = int(config['Settings'].get('window_width', '800'))
window_height = int(config['Settings'].get('window_height', '600'))

# メッセージ表示設定
messages_enabled = config['Settings'].get('messages', 'enable') == 'enable'

# 自動保存設定
autosave_json_enabled = config['Settings'].get('autosave_json', 'enable') == 'enable'

# 多言語対応のメッセージとラベル
messages = {
    'ja': {
        'add_parent': '親追加',
        'add_child': '子追加',
        'expand': '+',
        'collapse': '-',
        'delete': '削除',
        'update': '更新',
        'check_lock': 'ロック',
        'list': '一覧',
        'load': 'ロード',
        'save': 'セーブ',
        'copy': 'コピー',
        'shuffle': 'シャッフル',
        'clear': 'クリア',
        'tab_chunks': '  チャンク  ',
        'tab_words':  '    単語    ',
        'select_error': '選択エラー',
        'delete_error': '削除エラー',
        'update_error': '更新エラー',
        'update_complete': '更新完了',
        'copy_complete': 'コピー完了',
        'format_error': 'テキスト構文エラー',
        'unbalanced_brackets': '括弧が適切に閉じられていません。',
        'clear_confirm': 'クリア確認',
        'delete_confirm': '削除確認',
        'prompt_info': '情報',
        'prompt_listitemnotfound': '一覧表示できるファイルがありません。',
        'close': '閉じる',
        'prompt_created': '作成したプロンプトをクリップボードにコピーしました。',
        'prompt_cleared': '作成したプロンプトを消去します。本当によろしいですか？',
        'item_deleted': '選択したアイテムを削除します。削除していいですか？',
        'item_deleted_with_children': '配下のアイテムも一緒にすべて削除されます。削除していいですか？',
        'item_updated': 'アイテムが更新されました。',
        'item_exists': '他の親アイテムと内容が一致しています。同じ内容を登録することはできません。',
        'text_empty': 'テキストボックスが空です。',
        'select_item': '更新対象アイテムを選択してください。',
        'select_item_to_delete': '削除対象アイテムを選択してください。',
        'parent_needs_child': '親アイテムには最低一つの子アイテムが必要です。',
        'parent_needs_one': '親アイテムは最低一つ残す必要があります。',
        'check_autosave_json': '辞書オートセーブ',
        'save_json': '辞書セーブ',
        'exit_confirm': '終了前確認',
        'autosave_disabled_confirm': '\'辞書オートセーブ\'が無効になっています。アプリを終了してもいいですか？ \nアプリを終了する場合は\'OK\'を押してください。\n終了前に辞書を保存したい場合は\'キャンセル\'を押してから、\'辞書セーブ\'ボタンを押してください。'
    },
    'en': {
        'add_parent': 'Add Parent',
        'add_child': 'Add Child',
        'expand': '+',
        'collapse': '-',
        'delete': 'Delete',
        'update': 'Update',
        'check_lock': 'Lock',
        'list': 'List',
        'load': 'Load',
        'save': 'Save',
        'copy': 'Copy',
        'shuffle': 'Shuffle',
        'clear': 'Clear',
        'tab_chunks': '  Chunks  ',
        'tab_words':  '   Words   ',
        'select_error': 'Selection Error',
        'delete_error': 'Deletion Error',
        'update_error': 'Update Error',
        'update_complete': 'Update Completed',
        'copy_complete': 'Copy Complete',
        'format_error': 'Text format Error.',
        'unbalanced_brackets': 'Unbalanced brackets Error.',
        'clear_confirm': 'Clear Confirmation',
        'delete_confirm': 'Delete Confirmation',
        'prompt_info': 'Info',
        'prompt_listitemnotfound': 'No files found to list.',
        'close': 'Close',
        'prompt_created': 'Prompt copied to clipboard.',
        'prompt_cleared': 'Are you sure you want to clear the created prompt?',
        'item_deleted': 'Are you sure you want to delete the selected item?',
        'item_deleted_with_children': 'All items under the selected item will also be deleted. Are you sure?',
        'item_updated': 'Item has been updated.',
        'item_exists': 'Another parent item with the same content already exists. Cannot register the same content.',
        'text_empty': 'Text box is empty.',
        'select_item': 'Please select an item to update.',
        'select_item_to_delete': 'Please select an item to delete.',
        'parent_needs_child': 'A parent item must have at least one child item.',
        'parent_needs_one': 'At least one parent item must remain.',
        'check_autosave_json': 'Auto Save dicts.',
        'save_json': 'Save dicts.',
        'exit_confirm': 'Exit Confirmation',
        'autosave_disabled_confirm': '\'Auto save dicts.\' is disabled. Are you sure you want to exit the application? \nPress \'OK\' to Close App. \nPress \'CANCEL\' & \'Save dicts.\' if you want to save dictionary files before exit.'
    }
}

initial_data_chunks = {
    "Chunk Category 001": ["chunk 01","chunk 02","chunk 03"],
    "Chunk Category 002": ["chunk 01","chunk 02","chunk 03"],
    "Chunk Category 003": ["chunk 01","chunk 02","chunk 03"]
    }

initial_data_words = {
    "Words Category 001": ["word 01","word 02","word 03"],
    "Words Category 002": ["word 01","word 02","word 03"],
    "Words Category 003": ["word 01","word 02","word 03"]
    }


class PromptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Builder v" + version)
        self.root.geometry(f"{window_width}x{window_height}")

        # プロンプト欄のカーソル位置を記憶する
        def on_text_box_focus_out(self, event):
            self.cursor_position = self.text_box_bottom.index(tk.INSERT)
        # プロンプト欄のカーソル位置を記憶しておいた位置に戻す(再現する)
        def on_text_box_focus_in(self, event):
            if self.cursor_position:
                self.text_box_bottom.mark_set(tk.INSERT, self.cursor_position)
                self.text_box_bottom.see(tk.INSERT)

        # アプリ起動時に実行
        self.ensure_prompt_files_exist()

        self.undo_history = []  # UNDO用の履歴スタック
        self.redo_history = []  # REDO用の履歴スタック

        # ボタンの幅を統一
        self.button_width1 = 8

        style = ttk.Style()
        style.configure("Treeview", font=(textfont, fontsize_treeview))  # ツリービューのスタイル設定

        # 左右ペインを分割するためのPanedWindowを作成
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=10)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # 左ペイン (ツリービュー)
        self.left_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, width=300)

        # ボタンフレーム (左ペインの上部に配置)
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # 「親追加」ボタン
        self.add_parent_button = tk.Button(self.button_frame, text=messages[lang]['add_parent'], width=10, command=self.on_add_parent_button_click)
        self.add_parent_button.pack(side=tk.LEFT)

        # 「子追加」ボタン
        self.add_child_button = tk.Button(self.button_frame, text=messages[lang]['add_child'], width=10, command=self.on_add_child_button_click)
        self.add_child_button.pack(side=tk.LEFT)

        # 「展開」ボタン
        self.expand_button = tk.Button(self.button_frame, text=messages[lang]['expand'], width=1, command=self.expand_all)
        self.expand_button.pack(side=tk.LEFT)

        # 「閉じる」ボタン
        self.collapse_button = tk.Button(self.button_frame, text=messages[lang]['collapse'], width=1, command=self.collapse_all)
        self.collapse_button.pack(side=tk.LEFT)

        # 「削除」ボタン
        self.delete_button = tk.Button(self.button_frame, text=messages[lang]['delete'], width=6, command=self.on_delete_button_click)
        self.delete_button.pack(side=tk.RIGHT)

        # タブコントロールの作成
        self.tab_control = ttk.Notebook(self.left_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)

        # 左タブ (dict_chunks.json)
        self.left_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.left_tab, text=messages[lang]['tab_chunks'])

        # 右タブ (dict_words.json)
        self.right_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.right_tab, text=messages[lang]['tab_words'])

        # 左タブのツリービュー
        self.tree_left = ttk.Treeview(self.left_tab, style="Treeview")
        self.tree_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        # 左タブのスクロールバー
        self.tree_scrollbar_left = ttk.Scrollbar(self.left_tab, orient="vertical", command=self.tree_left.yview)
        self.tree_left.configure(yscrollcommand=self.tree_scrollbar_left.set)
        self.tree_scrollbar_left.pack(side=tk.RIGHT, fill=tk.Y)

        # 右タブのツリービュー
        self.tree_right = ttk.Treeview(self.right_tab, style="Treeview")
        self.tree_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 右タブのスクロールバー
        self.tree_scrollbar_right = ttk.Scrollbar(self.right_tab, orient="vertical", command=self.tree_right.yview)
        self.tree_right.configure(yscrollcommand=self.tree_scrollbar_right.set)
        self.tree_scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)

        # JSONファイルのロード
        self.load_dicts_from_json()

        # 前回選択したアイテムを記録する変数
        self.last_selected_parent = None
        self.last_selected_child = None

        # ツリービューの選択イベントをバインド
        self.tree_left.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree_right.bind("<<TreeviewSelect>>", self.on_tree_select)

        # ドラッグ＆ドロップのバインド
        self.tree_left.bind("<ButtonPress-1>", self.on_tree_item_press)
        self.tree_left.bind("<B1-Motion>", self.on_tree_item_motion)
        self.tree_left.bind("<ButtonRelease-1>", self.on_tree_item_release)
        self.tree_right.bind("<ButtonPress-1>", self.on_tree_item_press)
        self.tree_right.bind("<B1-Motion>", self.on_tree_item_motion)
        self.tree_right.bind("<ButtonRelease-1>", self.on_tree_item_release)

        # ドラッグデータの初期化
        self.drag_data = {"x": 0, "y": 0, "item": None, "tree": None}

        # 右ペイン
        self.right_frame = ttk.PanedWindow(self.paned_window, orient=tk.VERTICAL)
        self.paned_window.add(self.right_frame, minsize=200)  # 最小サイズを設定

        # 右ペインの上部フレーム (テキストボックスと「更新」ボタン)
        self.right_frame_top = tk.Frame(self.right_frame)
        self.right_frame.add(self.right_frame_top)

        # 「更新」ボタン
        self.update_button = tk.Button(self.right_frame_top, text=messages[lang]['update'], width=self.button_width1, command=self.on_update_button_click)
        self.update_button.pack(side=tk.LEFT, padx=5)

        # 上部テキストボックス
        self.text_box_top = tk.Text(self.right_frame_top, height=10)
        self.text_box_top.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_box_top.config(font=(textfont, fontsize_textbox))

        # 右ペインの下部フレーム (テキストボックスと「クリア」ボタン)
        self.right_frame_bottom = tk.Frame(self.right_frame)
        self.right_frame.add(self.right_frame_bottom)

        # 新しいフレームを作成してボタンを縦に配置
        self.button_vertical_frame = tk.Frame(self.right_frame_bottom)
        self.button_vertical_frame.pack(side=tk.LEFT, padx=5)

        # 「一覧」ボタンを追加
        self.list_button = tk.Button(self.button_vertical_frame, text=messages[lang]['list'], width=self.button_width1, command=self.on_list_button_click)
        self.list_button.pack(side=tk.TOP, pady=(5, 0))

        # ロードボタンの追加
        self.load_button = tk.Button(self.button_vertical_frame, text=messages[lang]['load'], width=self.button_width1, command=self.on_load_button_click)
        self.load_button.pack(side=tk.TOP, pady=(5, 0))

        # セーブボタンの追加
        self.save_button = tk.Button(self.button_vertical_frame, text=messages[lang]['save'], width=self.button_width1, command=self.on_save_button_click)
        self.save_button.pack(side=tk.TOP, pady=(5, 0))

        # 「コピー」ボタン
        self.copy_button = tk.Button(self.button_vertical_frame, text=messages[lang]['copy'], width=self.button_width1, command=self.on_copy_button_click)
        self.copy_button.pack(side=tk.TOP, pady=(60, 0))

        # 「シャッフル」ボタン
        self.shuffle_button = tk.Button(self.button_vertical_frame, text=messages[lang]['shuffle'], width=self.button_width1, command=self.on_shuffle_button_click)
        self.shuffle_button.pack(side=tk.TOP, pady=(5, 0))

        # ロックチェックボックスとラベル
        self.lock_var = tk.BooleanVar(value=False)  # ロック状態を管理する変数
        self.lock_checkbox = tk.Checkbutton(self.button_vertical_frame, text=messages[lang]['check_lock'], variable=self.lock_var, command=self.toggle_lock)
        self.lock_checkbox.pack(side=tk.TOP, pady=(60, 0))  # 上方向、間隔を少し広めに取る

        # 「クリア」ボタン
        self.clear_button = tk.Button(self.button_vertical_frame, text=messages[lang]['clear'], width=self.button_width1, command=self.on_clear_button_click)
        self.clear_button.pack(side=tk.TOP, pady=(5, 0))

        # 下部テキストボックス
        self.text_box_bottom = tk.Text(self.right_frame_bottom, height=10)
        self.text_box_bottom.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_box_bottom.config(state=tk.NORMAL)  # テキストボックスの編集状態を初期化
        self.text_box_bottom.config(font=(textfont, fontsize_textbox))  # システムフォントを使用

        # JSON自動保存設定のチェックボックス
        self.autosave_json_var = tk.BooleanVar(value=autosave_json_enabled)

        # チェックボックスとボタンを配置するフレーム
        self.json_options_frame = tk.Frame(self.left_frame)
        self.json_options_frame.pack(side=tk.BOTTOM, pady=5)

        self.autosave_json_checkbox = tk.Checkbutton(self.json_options_frame, text=messages[lang]['check_autosave_json'], variable=self.autosave_json_var, command=self.toggle_autosave_json)
        self.autosave_json_checkbox.pack(side=tk.LEFT)

        # JSON保存ボタン
        self.save_json_button = tk.Button(self.json_options_frame, text=messages[lang]['save_json'], width=10, command=self.save_dicts_to_json)
        self.save_json_button.pack(side=tk.RIGHT, padx=15)

        # JSONファイルのロード
        self.load_dicts_from_json()

        # 前回選択したアイテムを記録する変数
        self.last_selected_parent = None
        self.last_selected_child = None

        self.text_box_top.bind("<Control-Up>", self.on_ctrl_arrow_key)
        self.text_box_top.bind("<Control-Down>", self.on_ctrl_arrow_key)
        self.text_box_bottom.bind("<Control-Up>", self.on_ctrl_arrow_key)
        self.text_box_bottom.bind("<Control-Down>", self.on_ctrl_arrow_key)
        self.text_box_bottom.bind('<KeyRelease>', self.save_to_history1)

        self.root.bind("<Double-Button-1>", self.on_double_click)  # プロンプト欄では正常動作しなかったのでrootにbind(上のテキスト欄でも動作する)

        # タブ切り替え時のイベントをバインド
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # キーバインドの設定
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<Control-y>", self.redo)

        # 過去に自動保存されたtmpファイルを読み込む(text_box_bottomが配置された後でないと動作しないので注意)
        self.load_latest_prompt_file()


    def expand_selection(self, target_text):
        try:
            sel_start = target_text.index(tk.SEL_FIRST)
            sel_end = target_text.index(tk.SEL_LAST)
        except tk.TclError:
            # 選択範囲がない場合は何もしない
            return False

        # 行の内容を取得
        line_start = target_text.index(f"{sel_start} linestart")
        line_end = target_text.index(f"{sel_end} lineend")
        line_content = target_text.get(line_start, line_end)

        # 選択範囲の前後を検査
        start_offset = int(target_text.index(sel_start).split('.')[1])
        end_offset = int(target_text.index(sel_end).split('.')[1])
        before = line_content[:start_offset]
        after = line_content[end_offset:]

        # 括弧を探す
        open_paren = before.rfind('(')
        close_paren = after.find(')')

        if open_paren != -1 and close_paren != -1:
            # 開き括弧が見つからない場合（選択範囲が先頭から始まる場合）
            if open_paren == -1:
                new_start = line_start
            else:
                new_start = f"{line_start}+{open_paren}c"

            # 閉じ括弧が見つからない場合
            if close_paren == -1:
                new_end = line_end
            else:
                new_end = f"{sel_end}+{close_paren + 1}c"

            # 拡張後の内容を取得
            expanded_content = target_text.get(new_start, new_end)

            # ":数字" パターンをチェック
            match = re.search(r':([\d.]+)?\)$', expanded_content)
            if match:
                # ":数字" パターンが見つかった場合、それも含める
                new_end = f"{sel_end}+{close_paren + 1}c"

            target_text.tag_remove(tk.SEL, '1.0', tk.END)
            target_text.tag_add(tk.SEL, new_start, new_end)
            return True
        
        return False


    def on_ctrl_arrow_key(self, event):
        text_widget = event.widget
        
        try:
            start = text_widget.index(tk.SEL_FIRST)
            end = text_widget.index(tk.SEL_LAST)
            selected_text = text_widget.get(start, end)
        except tk.TclError:
            # return "break"  # 範囲指定されていない場合は何もせず、イベント伝播を停止
            # 選択範囲がない場合、カーソル位置の1単語を選択
            cursor_position = text_widget.index(tk.INSERT)
            word_start = text_widget.index(f"{cursor_position} wordstart")
            word_end = text_widget.index(f"{cursor_position} wordend")
            text_widget.tag_add(tk.SEL, word_start, word_end)  # 1単語を選択
            start = word_start
            end = word_end
            selected_text = text_widget.get(start, end)

        # 括弧で囲むか、数値を増減するかを判断
        if selected_text.startswith("(") and selected_text.endswith(")"):
            # 既に括弧で囲まれている場合、数値を増減
            new_text = self.modify_text(selected_text[1:-1], event.keysym == 'Up')
            text_widget.delete(start, end)
            text_widget.insert(start, f"({new_text})")
            # 選択範囲を維持
            text_widget.tag_add(tk.SEL, start, f"{start}+{len(new_text) + 2}c")
        else:
            # 選択範囲の拡張を試みる
            ret = self.expand_selection(text_widget)

            if ret==False:
                # 括弧で囲む
                new_text = f"({selected_text}:1.0)"
                text_widget.delete(start, end)
                text_widget.insert(start, new_text)
                # 選択範囲を維持
                text_widget.tag_add(tk.SEL, start, f"{start}+{len(new_text)}c")

        
        # カーソル位置を選択範囲の終わりに設定
        text_widget.mark_set(tk.INSERT, tk.SEL_LAST)
        # イベントの伝播を停止
        return "break"


    def modify_text(self, text, increase):
        # 数値部分を抽出
        match = re.search(r'^(.*?):(-?[\d.]+)$', text)
        if match:
            base_text = match.group(1)
            number = float(match.group(2))
        else:
            base_text = text
            number = 1.0

        # 数値を増減
        if increase:
            number += increment_unit
        else:
            number -= increment_unit

        # 数値のフォーマット
        if increment_unit == 0.1:
            number = round(number, 1)
        elif increment_unit == 0.05:
            number = round(number * 20) / 20  # 0.05単位で丸める
        else:
            number = round(number, 2)

        # 小数点以下の桁数を調整
        if number.is_integer():
            formatted_number = f"{number:.1f}"
        elif number * 10 % 1 == 0:
            formatted_number = f"{number:.1f}"
        else:
            formatted_number = f"{number:.2f}"

        new_text = f"{base_text}:{formatted_number}"
        return new_text


    def on_double_click(self, event):
        text_widget = event.widget
        
        # 現在の選択範囲を取得
        try:
            start = text_widget.index("sel.first")
            end = text_widget.index("sel.last")
        except tk.TclError:
            # 選択範囲がない場合は何もしない
            return

        # 選択されたテキストを取得
        selected_text = text_widget.get(start, end)

        # 末尾のカンマやピリオドを除去
        cleaned_text = re.sub(r'[,.]+$', '', selected_text)  # 末尾のカンマやピリオドをすべて削除

        # 新しい終了位置を計算
        new_end = f"{start}+{len(cleaned_text)}c"

        # 選択範囲を更新
        text_widget.tag_remove(tk.SEL, "1.0", tk.END)
        text_widget.tag_add(tk.SEL, start, new_end)

        selected_text = cleaned_text
        print(selected_text)

        return "break"  # デフォルトの動作を防ぐ


    def on_tree_select(self, event):
        tree = event.widget
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], "text")
            parent_item = tree.parent(selected_item[0])
            if parent_item:
                # 子アイテムが選択された場合
                self.text_box_top.delete(1.0, tk.END)
                self.text_box_top.insert(tk.END, item_text)

                # 前回選択したアイテムと同じなら下部テキストボックスに追加
                if self.last_selected_child == selected_item[0]:
                    item_text = item_text.rstrip(',') + ", "
                    cursor_position = self.text_box_bottom.index(tk.INSERT)
                    if cursor_position:
                        self.text_box_bottom.insert(cursor_position, item_text)
                    else:
                        self.text_box_bottom.insert(tk.END, item_text)
                    self.save_to_history2()
                else:
                    self.last_selected_child = selected_item[0]
                    self.last_selected_parent = parent_item
            else:
                self.text_box_top.delete(1.0, tk.END)
                self.text_box_top.insert(tk.END, item_text)
                self.last_selected_parent = selected_item[0]
                self.last_selected_child = None

    def expand_all(self):
        for tree in [self.tree_left, self.tree_right]:
            for item in tree.get_children():
                tree.item(item, open=True)
                self.expand_children(tree, item)

    def expand_children(self, tree, item):
        for child in tree.get_children(item):
            tree.item(child, open=True)
            self.expand_children(tree, child)

    def collapse_all(self):
        for tree in [self.tree_left, self.tree_right]:
            for item in tree.get_children():
                tree.item(item, open=False)
                self.collapse_children(tree, item)

    def collapse_children(self, tree, item):
        for child in tree.get_children(item):
            tree.item(child, open=False)
            self.collapse_children(tree, child)

    def on_tree_item_press(self, event):
        tree = event.widget
        self.drag_data = {"x": event.x, "y": event.y, "item": tree.identify_row(event.y), "tree": tree}
        self.is_dragging = True  # ドラッグ開始時に is_dragging を True に設定
        # ドラッグ開始時にアイテムを記録
        self.drag_start_item = self.drag_data["item"]

    def on_tree_item_motion(self, event):
        if "item" in self.drag_data and self.drag_data["item"]:
            x, y = event.x, event.y
            dx = abs(x - self.drag_data["x"])
            dy = abs(y - self.drag_data["y"])

            if dx > 20 or dy > 20:
                tree = self.drag_data["tree"]
                target_item = tree.identify_row(y)
                if target_item and target_item != self.drag_start_item:  # ドラッグ開始アイテムと異なる場合のみ移動
                    source_parent = tree.parent(self.drag_start_item)
                    target_parent = tree.parent(target_item)
                    if (source_parent == "" and target_parent == "") or (source_parent != "" and target_parent != ""):
                        tree.move(self.drag_start_item, tree.parent(target_item), tree.index(target_item))

                self.drag_data["x"] = x
                self.drag_data["y"] = y
        # print(self.drag_data["item"])

    def on_tree_item_release(self, event):
        self.drag_data = {"x": 0, "y": 0, "item": None, "tree": None}
        self.is_dragging = False  # ドラッグ終了時に is_dragging を False に設定
        if autosave_json_enabled:
            self.save_dicts_to_json()

    def on_add_parent_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        tree = self.tree_left if current_tab == 0 else self.tree_right
        parent_count = len(tree.get_children()) + 1
        parent_text = f"Genre {parent_count}" if current_tab == 0 else f"Category {parent_count}"
        parent_item = tree.insert("", "end", text=parent_text)
        
        # 小アイテムを3つ追加
        for child_count in range(1, 4):  # 1から3までのループ
            tree.insert(parent_item, "end", text=str(child_count))  # 子アイテムを追加
        
        tree.item(parent_item, open=True)  # 親アイテムを展開
        tree.selection_set(parent_item)  # 追加した親アイテムを選択状態にする
        # tree.selection_set(child_item)  # 子アイテムの選択を解除
        if autosave_json_enabled:
            self.save_dicts_to_json()
        # 追加したアイテムにフォーカスを移動
        tree.focus(parent_item)

    def on_add_child_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        tree = self.tree_left if current_tab == 0 else self.tree_right
        selected_item = tree.selection()
        if not selected_item:
            if messages_enabled:
                messagebox.showinfo(messages[lang]['select_error'], messages[lang]['select_item_to_delete'])
            return

        parent_item = tree.parent(selected_item[0])
        if parent_item:
            parent_item = parent_item
        else:
            parent_item = selected_item[0]

        children = tree.get_children(parent_item)
        child_count = len(children) + 1
        child_item = tree.insert(parent_item, "end", text=str(child_count))  # 子アイテムを追加
        tree.item(parent_item, open=True)  # 親アイテムを展開
        tree.selection_set(child_item)  # 追加した子アイテムを選択状態にする
        if autosave_json_enabled:
            self.save_dicts_to_json()
        # 追加したアイテムにフォーカスを移動
        tree.focus(child_item)

    def on_delete_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        tree = self.tree_left if current_tab == 0 else self.tree_right
        selected_item = tree.selection()
        if not selected_item:
            if messages_enabled:
                messagebox.showinfo(messages[lang]['delete_error'], messages[lang]['select_item_to_delete'])
            return

        parent_item = tree.parent(selected_item[0])
        if parent_item:
            children = tree.get_children(parent_item)
            if len(children) == 1:
                if messages_enabled:
                    messagebox.showinfo(messages[lang]['delete_error'], messages[lang]['parent_needs_child'])
                return
            else:
                result = messagebox.askokcancel(messages[lang]['delete_confirm'], messages[lang]['item_deleted'])
                if result:
                    # 削除前に前後のアイテムを記憶しておく
                    previous_item = tree.prev(selected_item[0])
                    next_item = tree.next(selected_item[0])
                    # 削除したアイテムの上のアイテムにフォーカスを移動
                    if previous_item:
                        tree.focus(previous_item)
                        tree.selection_set(previous_item)  # 削除したアイテムの上のアイテムを選択状態にする
                    else:
                        # 上のアイテムがない場合は下のアイテムにフォーカスを移動
                        if next_item:
                            tree.focus(next_item)
                            tree.selection_set(next_item)  # 削除したアイテムの下のアイテムを選択状態にする

                    tree.delete(selected_item[0])
                    if autosave_json_enabled:
                        self.save_dicts_to_json()
                    
                    print("1")
        else:
            children = tree.get_children(selected_item[0])
            if len(tree.get_children()) == 1:
                if messages_enabled:
                    messagebox.showinfo(messages[lang]['delete_error'], messages[lang]['parent_needs_one'])
                return
            elif children:
                result = messagebox.askokcancel(messages[lang]['delete_confirm'], messages[lang]['item_deleted_with_children'])
                if result:
                    # 削除前に前後のアイテムを記憶しておく
                    previous_item = tree.prev(selected_item[0])
                    next_item = tree.next(selected_item[0])
                    # 削除したアイテムの上のアイテムにフォーカスを移動
                    if previous_item:
                        tree.focus(previous_item)
                        tree.selection_set(previous_item)  # 削除したアイテムの上のアイテムを選択状態にする
                    else:
                        # 上のアイテムがない場合は下のアイテムにフォーカスを移動
                        if next_item:
                            tree.focus(next_item)
                            tree.selection_set(next_item)  # 削除したアイテムの下のアイテムを選択状態にする

                    tree.delete(selected_item[0])
                    if autosave_json_enabled:
                        self.save_dicts_to_json()
                    
                    print("2")
            else:
                # 削除前に前後のアイテムを記憶しておく
                previous_item = tree.prev(selected_item[0])
                next_item = tree.next(selected_item[0])
                # 削除したアイテムの上のアイテムにフォーカスを移動
                if previous_item:
                    tree.focus(previous_item)
                    tree.selection_set(previous_item)  # 削除したアイテムの上のアイテムを選択状態にする
                else:
                    # 上のアイテムがない場合は下のアイテムにフォーカスを移動
                    if next_item:
                        tree.focus(next_item)
                        tree.selection_set(next_item)  # 削除したアイテムの下のアイテムを選択状態にする

                tree.delete(selected_item[0])
                if autosave_json_enabled:
                    self.save_dicts_to_json()

                print("3")


    def on_update_button_click(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        tree = self.tree_left if current_tab == 0 else self.tree_right
        selected_item = tree.selection()
        if not selected_item:
            if messages_enabled:
                messagebox.showinfo(messages[lang]['update_error'], messages[lang]['select_item'])
            return

        new_text = self.text_box_top.get(1.0, tk.END).strip()
        if not new_text:
            if messages_enabled:
                messagebox.showinfo(messages[lang]['update_error'], messages[lang]['text_empty'])
            return

        parent_item = tree.parent(selected_item[0])
        if not parent_item:
            for item in tree.get_children():
                if item != selected_item[0] and tree.item(item, "text") == new_text:
                    if messages_enabled:
                        messagebox.showinfo(messages[lang]['update_error'], messages[lang]['item_exists'])
                    return

        tree.item(selected_item[0], text=new_text)
        if autosave_json_enabled:
            self.save_dicts_to_json()
        if messages_enabled:
            messagebox.showinfo(messages[lang]['update_complete'], messages[lang]['item_updated'])

    def on_list_button_click(self):
        prompt_folder = 'prompt'
        files = glob(os.path.join(prompt_folder, "prompt_saved_*.txt"))
        
        if not files:
            messagebox.showinfo(messages[lang]['prompt_info'], messages[lang]['prompt_listitemnotfound'])
            return

        # 最新の5つのファイルを取得
        files.sort(key=os.path.getctime, reverse=True)
        latest_files = files[:5]

        # 新しいウィンドウを作成
        self.list_window = tk.Toplevel(self.root)
        self.list_window.title("Saved Prompts")

        # ボタンを縦に並べるフレーム
        self.button_frame2 = tk.Frame(self.list_window)
        self.button_frame2.pack(padx=10, pady=10)

        # 各ファイルに対するボタンを作成
        for file in latest_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                button = tk.Button(self.button_frame2, text=content, command=lambda c=content: self.open_prompt(c), width=80)
                button.pack(pady=5)

        # ページ切り替えボタン用のフレームを作成
        self.page_button_frame = tk.Frame(self.list_window)
        self.page_button_frame.pack(side=tk.BOTTOM, pady=5)

        # ページ切り替えボタンの作成
        total_files = len(files)
        pages = (total_files - 1) // 5 + 1

        for i in range(pages):
            page_button = tk.Button(self.page_button_frame, text=str(i + 1), command=lambda p=i: self.load_page(files, p), width=3)
            page_button.pack(side=tk.LEFT, padx=5)

        # 閉じるボタンを右端に配置
        close_button = tk.Button(self.page_button_frame, text=messages[lang]['close'], command=self.list_window.destroy, width=self.button_width1)
        close_button.pack(side=tk.RIGHT, padx=5)

    def load_page(self, files, page):
        # ページに応じてファイルを表示
        start_index = page * 5
        end_index = start_index + 5
        latest_files = files[start_index:end_index]

        # 既存のボタンをクリア
        for widget in self.button_frame2.winfo_children():
            widget.destroy()

        # 新しいボタンを作成
        for file in latest_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                button = tk.Button(self.button_frame2, text=content, command=lambda c=content: self.open_prompt(c), width=80)
                button.pack(pady=5)

        # ページ切り替えボタンをクリア
        for widget in self.page_button_frame.winfo_children():
            widget.destroy()

        total_files = len(files)
        pages = (total_files - 1) // 5 + 1

        for i in range(pages):
            page_button = tk.Button(self.page_button_frame, text=str(i + 1), command=lambda p=i: self.load_page(files, p), width=3)
            page_button.pack(side=tk.LEFT, padx=5)

        # 閉じるボタンを右端に配置
        close_button = tk.Button(self.page_button_frame, text=messages[lang]['close'], command=self.list_window.destroy, width=self.button_width1)
        close_button.pack(side=tk.RIGHT, padx=5)

    def open_prompt(self, content):
        # プロンプトをテキストボックスに表示
        self.text_box_bottom.delete(1.0, tk.END)
        self.text_box_bottom.insert(tk.END, content)

    def on_load_button_click(self):
        from tkinter import filedialog
        
        default_directory = 'prompt'
        file_path = filedialog.askopenfilename(defaultextension=".txt", initialdir=default_directory, filetypes=[("Text files", "*.txt")])
        
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_box_bottom.delete(1.0, tk.END)
                self.text_box_bottom.insert(tk.END, content)
                self.undo_history.clear()
                self.redo_history.clear()
                self.undo_history.append(content)
            if messages_enabled:
                messagebox.showinfo(messages[lang]['load'], "ファイルを読み込みました。")

    def on_save_button_click(self):
        if not self.text_box_bottom.get(1.0, tk.END).strip():
            if messages_enabled:
                messagebox.showinfo(messages[lang]['save'], messages[lang]['text_empty'])
            return
        
        from tkinter import filedialog
        import datetime
        
        default_directory = 'prompt'
        default_filename = f"prompt_saved_{datetime.datetime.now().strftime(config['Settings']['datetime_format'])}.txt"
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=default_directory, initialfile=default_filename)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                # file.write(self.text_box_bottom.get(1.0, tk.END).strip())
                file.write(self.text_box_bottom.get(1.0, tk.END))  # ファイル末尾の空白をそのまま残したいのでこちらを採用
            if messages_enabled:
                messagebox.showinfo(messages[lang]['save'], "ファイルを保存しました。")

    def on_copy_button_click(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_box_bottom.get(1.0, tk.END).strip())
        self.root.update()
        if messages_enabled:
            messagebox.showinfo(messages[lang]['copy_complete'], messages[lang]['prompt_created'])

    def on_shuffle_button_click(self):
        # プロンプト欄のテキストを取得
        text = self.text_box_bottom.get("1.0", tk.END).strip()

        # 選択範囲があるか確認
        try:
            start = self.text_box_bottom.index(tk.SEL_FIRST)
            end = self.text_box_bottom.index(tk.SEL_LAST)
            selected_text = self.text_box_bottom.get(start, end)
            text_to_shuffle = selected_text
        except tk.TclError:
            start = "1.0"  # 選択範囲がない場合は全体を対象とする
            end = "end"
            text_to_shuffle = text

        # 括弧で囲まれた単語を分割
        words = self.split_words(text_to_shuffle)

        # 括弧が適切に閉じられていない場合はメッセージを表示して処理を終了
        if not words:
            # split_wordsのほうでメッセージ出すのでここはコメントアウト
            # messagebox.showinfo(messages[lang]['format_error'], messages[lang]['unbalanced_brackets'])
            return

        # 単語をシャッフル
        random.shuffle(words)

        # シャッフル後のテキストを結合
        shuffled_text = ", ".join(words).strip(", ")  # スペース区切りからカンマ区切りに変更し、末尾のカンマを削除

        # 末尾が単語で終わっている場合、", "を追加
        if shuffled_text:
            shuffled_text += ", "

        # 選択範囲がある場合は選択範囲を更新
        try:
            self.text_box_bottom.delete(start, end)
            self.text_box_bottom.insert(start, shuffled_text)
            self.text_box_bottom.tag_add(tk.SEL, start, f"{start}+{len(shuffled_text)}c")
        except tk.TclError:
            # 選択範囲がない場合は全体を更新
            self.text_box_bottom.delete("1.0", tk.END)
            self.text_box_bottom.insert(tk.END, shuffled_text)

        # 履歴を保存
        self.save_to_history2()

    def split_words(self, text):
        # 括弧で囲まれた単語を分割する関数
        words = []
        current_word = ""
        bracket_stack = []
        for char in text:
            if char in "({[<":
                bracket_stack.append(char)
                current_word += char
            elif char in ")}]>":
                if bracket_stack:
                    # 括弧の対応関係をチェック
                    if (bracket_stack[-1] == "(" and char == ")") or \
                       (bracket_stack[-1] == "{" and char == "}") or \
                       (bracket_stack[-1] == "[" and char == "]") or \
                       (bracket_stack[-1] == "<" and char == ">"):
                        bracket_stack.pop()
                        current_word += char
                    else:
                        # 括弧が閉じられていない場合はエラー処理
                        messagebox.showinfo(messages[lang]['format_error'], messages[lang]['unbalanced_brackets'])
                        return []  # 空のリストを返す
                else:
                    # 括弧が閉じられていない場合はエラー処理
                    messagebox.showinfo(messages[lang]['format_error'], messages[lang]['unbalanced_brackets'])
                    return []  # 空のリストを返す
            elif char == "," and not bracket_stack:
                words.append(current_word.strip())
                current_word = ""
            else:
                current_word += char

        if current_word:
            words.append(current_word.strip())

        # もし括弧が閉じられていない場合、最後の単語を追加
        if bracket_stack:
            messagebox.showinfo(messages[lang]['format_error'], messages[lang]['unbalanced_brackets'])
            return []  # 空のリストを返す

        return words
    
    def toggle_lock(self):
        if self.lock_var.get():
            self.text_box_bottom.config(state=tk.DISABLED)  # 編集不可にする
            self.clear_button.config(state=tk.DISABLED)  # クリアボタンを無効にする
        else:
            self.text_box_bottom.config(state=tk.NORMAL)  # 編集可能にする
            self.clear_button.config(state=tk.NORMAL)  # クリアボタンを有効にする

    def on_clear_button_click(self):
        result = messagebox.askokcancel(messages[lang]['clear_confirm'], messages[lang]['prompt_cleared'])
        if result:
            self.text_box_bottom.delete(1.0, tk.END)

    def ensure_prompt_files_exist(self):
        # dict_chunks.jsonの存在チェックと作成
        if not os.path.exists('dict_chunks.json'):
            with open('dict_chunks.json', 'w', encoding='utf-8') as file:
                json.dump(initial_data_chunks, file, ensure_ascii=False, indent=4)
        else:
            pass

        # dict_words.jsonの存在チェックと作成
        if not os.path.exists('dict_words.json'):
            with open('dict_words.json', 'w', encoding='utf-8') as file:
                json.dump(initial_data_words, file, ensure_ascii=False, indent=4)
        else:
            pass

        # bkフォルダの存在チェックと作成
        if not os.path.exists('bk'):
            os.makedirs('bk')
        else:
            pass

        # promptフォルダの存在チェックと作成
        if not os.path.exists('prompt'):
            os.makedirs('prompt')
        else:
            pass

        # バックアップ設定の確認
        if config['Settings']['backup_json'] == 'enable':
            # dict_chunks.jsonのバックアップ
            with open('dict_chunks.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            with open('bk/dict_chunks_bk.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            # dict_words.jsonのバックアップ
            with open('dict_words.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            with open('bk/dict_words_bk.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

    def load_dicts_from_json(self):
        # 左タブのツリービューをクリア
        for item in self.tree_left.get_children():
            self.tree_left.delete(item)

        # dict_chunks.jsonの読み込み
        with open('dict_chunks.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for parent, children in data.items():
                parent_item = self.tree_left.insert("", "end", text=parent)
                for child in children:
                    self.tree_left.insert(parent_item, "end", text=child)

        # 右タブのツリービューをクリア
        for item in self.tree_right.get_children():
            self.tree_right.delete(item)

        # dict_words.jsonの読み込み
        with open('dict_words.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for parent, children in data.items():
                parent_item = self.tree_right.insert("", "end", text=parent)
                for child in children:
                    self.tree_right.insert(parent_item, "end", text=child)

    def save_dicts_to_json(self):
        # dict_chunks.jsonの保存
        data_left = {}
        for parent_item in self.tree_left.get_children():
            parent_text = self.tree_left.item(parent_item, "text")
            children_texts = [self.tree_left.item(child, "text") for child in self.tree_left.get_children(parent_item)]
            data_left[parent_text] = children_texts

        with open('dict_chunks.json', 'w', encoding='utf-8') as file:
            json.dump(data_left, file, ensure_ascii=False, indent=4)

        # dict_words.jsonの保存
        data_right = {}
        for parent_item in self.tree_right.get_children():
            parent_text = self.tree_right.item(parent_item, "text")
            children_texts = [self.tree_right.item(child, "text") for child in self.tree_right.get_children(parent_item)]
            data_right[parent_text] = children_texts

        with open('dict_words.json', 'w', encoding='utf-8') as file:
            json.dump(data_right, file, ensure_ascii=False, indent=4)

    def on_tab_changed(self, event):
        current_tab = self.tab_control.index(self.tab_control.select())
        tree = self.tree_left if current_tab == 0 else self.tree_right
        selected_item = tree.selection()
        if selected_item:
            item_text = tree.item(selected_item[0], "text")
            self.text_box_top.delete(1.0, tk.END)
            self.text_box_top.insert(tk.END, item_text)
        else:
            self.text_box_top.delete(1.0, tk.END)


    def load_latest_prompt_file(self):
        prompt_folder = 'prompt'
        if not os.path.exists(prompt_folder):  # フォルダの存在確認
            return

        pattern = os.path.join(prompt_folder, "prompt_tmp_*.txt")
        files = glob(pattern)

        if files:
            latest_file = max(files, key=os.path.getctime)
            
            try:
                with open(latest_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if content:  # 中身が空でないことを確認
                        self.text_box_bottom.delete(1.0, tk.END)
                        self.text_box_bottom.insert(tk.END, content)
                    self.undo_history.clear()
                    self.redo_history.clear()
                    self.undo_history.append(content)
            except Exception as e:
                print(f"Error reading file: {e}")  # エラーメッセージを表示

    # バインド用履歴保存処理(プロンプト欄の直接のテキスト編集を監視するのに使う)
    def save_to_history1(self, event=None):
        content = self.text_box_bottom.get("1.0", tk.END).strip()
        if not self.undo_history or content != self.undo_history[-1]:
            self.undo_history.append(content)
            self.redo_history.clear()

    # 普通呼び出し用履歴保存処理(ツリーからのアイテム選択によるチャンク・単語追加時に使う)
    def save_to_history2(self):
        content = self.text_box_bottom.get("1.0", tk.END).strip()
        if not self.undo_history or content != self.undo_history[-1]:
            self.undo_history.append(content)
            self.redo_history.clear()

    def undo(self, event=None):
        if len(self.undo_history) > 1:
            self.redo_history.append(self.undo_history.pop())
            self.text_box_bottom.delete("1.0", tk.END)
            self.text_box_bottom.insert(tk.END, self.undo_history[-1])

    def redo(self, event=None):
        if self.redo_history:
            self.undo_history.append(self.redo_history.pop())
            self.text_box_bottom.delete("1.0", tk.END)
            self.text_box_bottom.insert(tk.END, self.undo_history[-1])

    def toggle_autosave_json(self):
        global autosave_json_enabled
        autosave_json_enabled = self.autosave_json_var.get()
        config['Settings']['autosave_json'] = 'enable' if autosave_json_enabled else 'disable'
        with open(settings_path, 'w') as configfile:
            config.write(configfile)

    def save_dicts_to_json(self):
        # dict_chunks.jsonの保存
        data_left = {}
        for parent_item in self.tree_left.get_children():
            parent_text = self.tree_left.item(parent_item, "text")
            children_texts = [self.tree_left.item(child, "text") for child in self.tree_left.get_children(parent_item)]
            data_left[parent_text] = children_texts

        with open('dict_chunks.json', 'w', encoding='utf-8') as file:
            json.dump(data_left, file, ensure_ascii=False, indent=4)

        # dict_words.jsonの保存
        data_right = {}
        for parent_item in self.tree_right.get_children():
            parent_text = self.tree_right.item(parent_item, "text")
            children_texts = [self.tree_right.item(child, "text") for child in self.tree_right.get_children(parent_item)]
            data_right[parent_text] = children_texts

        with open('dict_words.json', 'w', encoding='utf-8') as file:
            json.dump(data_right, file, ensure_ascii=False, indent=4)

    def save_prompt_and_close(self):
        import datetime
        import glob

        # 古いtmpファイルを削除
        old_files = glob.glob('prompt/prompt_tmp_*.txt')
        for old_file in old_files:
            os.remove(old_file)

        default_directory = 'prompt'
        default_filename = f"prompt_tmp_{datetime.datetime.now().strftime(config['Settings']['datetime_format'])}.txt"
        file_path = os.path.join(default_directory, default_filename)
        

        content = self.text_box_bottom.get(1.0, tk.END)  # 末尾の空白を残すためにrstripしない

        # 末尾の改行を一つだけに置換
        content = content.rstrip("\n") + "\n" if content.endswith("\n") else content

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)  # ファイルに内容を書き込む
        
        # 少し待ってからウィンドウを閉じる
        self.root.after(100, self.root.destroy)
    
    def on_exit(self):

        if not autosave_json_enabled:
            result = messagebox.askokcancel(messages[lang]['exit_confirm'], messages[lang]['autosave_disabled_confirm'])
            if result:
                # 空でもtmpファイル作る
                self.save_prompt_and_close()
                self.root.destroy()
            else:
                return
        else:
            # 空でもtmpファイル作る
            self.save_prompt_and_close()
            self.root.destroy()
        
    def start(self):
        self.ensure_prompt_files_exist()
        self.load_dicts_from_json()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # フォント設定(tkFontのインポートをrootウインドウ作成後に行う必要があるため、ここで実施)
        textfont = config['Settings']['textfont']
        try:
            tkFont.Font(family=textfont)
        except tk.TclError:
            textfont = 'TkDefaultFont'  # 利用できないフォントならTkinterのデフォルトフォントを使用

        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = PromptApp(root)
    app.start()
